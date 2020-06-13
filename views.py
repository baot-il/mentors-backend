from app import app
from flask import request, g
from flask_cors import cross_origin
from models import Mentor, Mentee, Match, Technology, Users
from peewee import DoesNotExist, IntegrityError
from playhouse.shortcuts import model_to_dict
import firebase_admin
from firebase_admin import auth
import os
from functools import wraps

YEARS_EXPERIENCE = ['1-2', '3-4', '5-7', '8-10', '10+']
MANAGER = 'manager'
MENTOR = 'mentor'

firebase_app = firebase_admin.initialize_app()

def parse_token(headers):
    decoded_token = None
    if 'Authorization' in headers:
        idToken = headers['Authorization'].split(" ")[1]
        decoded_token = auth.verify_id_token(idToken)
    return decoded_token

@app.before_request
def authenticate():
    if app.config["DEVELOPMENT"]:
        return
    if request.method == "OPTIONS":
        return 'ok', 200
    decoded_token = parse_token(request.headers)
    if decoded_token:
        g.is_manager = add_custom_claims(decoded_token)
        g.uid = decoded_token['uid']
    else:
        return 'Unauthorised user', 403

def add_custom_claims(decoded_token):
    # TODO: in future versions, add a UI screen for admins to add 
    # managers, and remove from environment variables.
    claims = decoded_token
    if claims[MANAGER]:
        return True
    if claims[MENTOR]:
        return False

    managers = os.environ['MANAGERS'].split(',')
    if True in [decoded_token['email'] == email for email in managers]:
        auth.set_custom_user_claims(uid, {MANAGER: True})
        return True
    auth.set_custom_user_claims(uid, {MENTOR: True})
    return False

@manager_access
@app.route('/resetCustomClaims', methods=['GET'])
    def modify_custom_claims():
        email_to_reset = request.args.get('email')
        user = auth.get_user_by_email(email)
        auth.set_custom_user_claims(user.uid, {})

def manager_access(view_function):
  @wraps(view_function)
  def wrapper(*args, **kwargs):
    if not g.is_manager:
      abort(403, "This end point is not allowed to users with your permissions.")
    return view_function(*args, **kwargs)
  return wrapper

@app.route('/')
def homepage():
    return 'Hello World!'

@app.route('/user', methods=['GET', 'POST'])
@cross_origin()
def user():
    uid = g.uid
    user = auth.get_user(uid)
    if not user or not user.email:
        return 'Invalid user', 403
    if request.method == 'GET':
        try:
            user = Users.select().where(Users.uid == uid).dicts().get()
            return {'user': user}
        except DoesNotExist:
            return {'user': None}
    elif request.method == 'POST':
        user, _ = Users.get_or_create(uid=uid)
        return {'user': model_to_dict(user)}
    return 'Unsupported method {}'.format(request.method), 405

@app.route('/technologies', methods=['GET', 'POST'])
@cross_origin()
def technologies():
    if request.method == 'GET':
        return {'technologies': [t.name for t in Technology.select()]}
    else:
        technologies_str = request.form.get('technologies', '')
        technologies_list = [t.strip() for t in technologies_str.split(',')]
        inserted = Technology.insert_many([{'name': tech}
                                           for tech in technologies_list]).returning().on_conflict_ignore().execute()
        return '{} technologies inserted'.format(inserted)


@app.route('/mentors', methods=['GET', 'POST'])
@manager_access
@cross_origin()
def mentors():
    if request.method == 'GET':
        return {'mentors': [mentor_dict for mentor_dict in Mentor.select().dicts()]}
    mentor_data = request.form
    if request.method == 'POST':
        try:
            Mentor.insert(mentor_data).execute()
            return 'Success'
        except IntegrityError:
            return 'Mentor exists (email)', 409


@app.route('/mentor', methods=['GET', 'PUT'])
def get_mentor_by_uid():
    uid = g.uid
    if request.method == 'GET':
        try:
            user = Users.select(Users.mentor_id).where(Users.uid == uid).get()
            return {'mentors': Mentor.select().where(Mentor.id == user.mentor_id).dicts().get()}
        except DoesNotExist:
            return {'mentors': []}
    elif request.method == 'PUT':
        mentor_data = request.json
        try:
            user = Users.select(Users.mentor_id).where(Users.uid == uid).get()
            Mentor.select().where(Mentor.id == user.mentor_id).dicts().get()
            exists = True
        except DoesNotExist:
            exists = False

        try:
            if exists:
                updated = Mentor.update(mentor_data).where(Mentor.id == user.mentor_id).execute()
                updated_user = Users.update(mentor_id=updated).where(Users.uid == uid).execute()
            else:
                updated = Mentor.insert(mentor_data).execute()
                updated_user = Users.insert(uid=uid, mentor_id=updated, is_manager=False, is_admin=False).execute()
        except Exception as e:
            return f'Failed with error: {e}', 409
        return 'Success' if updated else 'Non updated'


@app.route('/years_experience', methods=['GET'])
@cross_origin()
def get_years_experience():
    return {'years_experience': YEARS_EXPERIENCE}
