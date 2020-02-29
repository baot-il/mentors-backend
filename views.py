from app import app
from flask import request
from flask_cors import cross_origin
from models import Mentor, Mentee, Match, Technology
from peewee import DoesNotExist, IntegrityError


YEARS_EXPERIENCE = ['1-2', '3-4', '5-7', '8-10', '10+']


@app.route('/')
def homepage():
    return 'Hello World!'


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
    if request.method == 'POST':
        mentor_data = request.form
        try:
            Mentor.insert(mentor_data).execute()
        except IntegrityError:
            return 'Mentor exists (email)', 409
    else:
        return {'mentors': [mentor_dict for mentor_dict in Mentor.select().dicts()]}


@app.route('/mentors/<mentor_id>')
def get_mentor_by_id(mentor_id):
    try:
        return {'mentors': Mentor.select().where(Mentor.id == mentor_id).dicts().get()}
    except DoesNotExist:
        return {'mentors': []}


@app.route('/years_experience', methods=['GET'])
def get_years_experience():
    return {'years_experience': YEARS_EXPERIENCE}
