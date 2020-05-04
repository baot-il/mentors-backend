from app import app
from flask import request, g
from flask_cors import cross_origin
from models import Mentor, Mentee, Match, Technology, Users
from peewee import DoesNotExist, IntegrityError
from playhouse.shortcuts import model_to_dict
import firebase_admin
from firebase_admin import auth

YEARS_EXPERIENCE = ['1-2', '3-4', '5-7', '8-10', '10+']

firebase_app = firebase_admin.initialize_app()

@app.before_request
def authenticate():
    if request.method == "OPTIONS":
        return 'ok', 200
    headers = request.headers
    is_valid = False
    if 'Authorization' in headers:
        idToken = headers['Authorization'].split(" ")[1]
        decoded_token = auth.verify_id_token(idToken)
        if decoded_token:
            g.uid = decoded_token['uid']
            is_valid = True
    if not is_valid:
        return 'Unauthorised user', 403

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


@app.route('/mentors/<mentor_id>', methods=['GET', 'PUT'])
def get_mentor_by_id(mentor_id):
    if request.method == 'GET':
        try:
            return {'mentors': Mentor.select().where(Mentor.id == mentor_id).dicts().get()}
        except DoesNotExist:
            return {'mentors': []}
    elif request.method == 'PUT':
        mentor_data = request.json
        try:
            Mentor.select().where(Mentor.id == mentor_id).dicts().get()
            exists = True
        except DoesNotExist:
            exists = False

        if exists:
            updated = Mentor.update(mentor_data).where(Mentor.id == mentor_id).execute()
        else:
            updated = Mentor.insert(mentor_data).execute()
        return 'Success' if updated else 'Non updated'


@app.route('/years_experience', methods=['GET'])
@cross_origin()
def get_years_experience():
    return {'years_experience': YEARS_EXPERIENCE}
