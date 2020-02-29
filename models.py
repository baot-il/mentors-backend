from app import db
from peewee import Model, AutoField, BooleanField, CompositeKey, DateTimeField, ForeignKeyField, TextField
from playhouse.postgres_ext import ArrayField
import datetime


class BaseModel(Model):
    class Meta:
        database = db


class Mentor(BaseModel):
    id = AutoField(primary_key=True)
    full_name = TextField(index=True)
    email = TextField(index=True)
    phone = TextField()
    created_on = DateTimeField(default=datetime.datetime.now)
    workplace = TextField(null=True)
    job_title = TextField(null=True)
    bio = TextField(null=True)
    academic_bio = TextField(null=True)
    job_search = TextField(null=True)
    availability = TextField(null=True)
    match_preferences = TextField(null=True)
    multiple_mentees = BooleanField(default=False)
    can_simulate = BooleanField(default=False)
    technologies = ArrayField(field_class=TextField, null=True)
    years_experience = TextField(null=True)
    comments = TextField(null=True)


class Mentee(BaseModel):
    id = AutoField(primary_key=True)
    full_name = TextField(index=True)
    email = TextField(index=True)
    phone = TextField()
    created_on = DateTimeField(default=datetime.datetime.now)
    bio = TextField(null=True)
    academic_bio = TextField(null=True)
    job_search = TextField(null=True)
    technologies = ArrayField(field_class=TextField, null=True)
    years_experience = TextField(null=True)
    comments = TextField(null=True)


class Technology(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField(index=True, unique=True)


class Match(BaseModel):
    mentor_id = ForeignKeyField(Mentor, lazy_load=False)
    mentee_id = ForeignKeyField(Mentee, lazy_load=False)
    start_time = DateTimeField(null=True)
    end_time = DateTimeField(null=True)

    class Meta:
        primary_key = CompositeKey('mentor_id', 'mentee_id')
