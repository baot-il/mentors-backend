from extensions import db
import datetime as dt
from sqlalchemy.dialects import postgresql as pg


class Technology(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.Text(), nullable=False)
    email = db.Column(db.Text(), nullable=False)
    phone = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, index=True, default=dt.datetime.utcnow)
    workplace = db.Column(db.Text())
    job_title = db.Column(db.Text())
    bio = db.Column(db.Text())
    academic_bio = db.Column(db.Text())
    job_search = db.Column(db.Text())
    availability = db.Column(db.Text())
    match_preferences = db.Column(db.Text())
    multiple_mentees = db.Column(db.Boolean())
    can_simulate = db.Column(db.Boolean())
    technologies = db.Column(pg.ARRAY(db.String, dimensions=1))
    years_experience = db.Column(db.Text())
    comments = db.Column(db.Text())

    def __init__(self, full_name, email, phone):
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.created_on = dt.datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Mentee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.Text(), nullable=False)
    email = db.Column(db.Text(), nullable=False)
    phone = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, index=True, default=dt.datetime.utcnow)
    bio = db.Column(db.Text())
    academic_bio = db.Column(db.Text())
    job_search = db.Column(db.Text())
    technologies = db.Column(pg.ARRAY(db.String, dimensions=1))
    years_experience = db.Column(db.Text())
    comments = db.Column(db.Text())

    def __init__(self, full_name, email, phone):
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.created_on = dt.datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Match(db.Model):
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'), primary_key=True)
    mentee_id = db.Column(db.Integer, db.ForeignKey('mentee.id'), primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    
    def __init__(self, mentor_id, mentee_id, start_time, end_time):
        self.mentor_id = mentor_id
        self.mentee_id = mentee_id
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return '<match: {}->{}>'.format(self.mentor_id, self.mentee_id)
