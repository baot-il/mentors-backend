import datetime

from peewee import Model, AutoField, BooleanField, CompositeKey, DateTimeField, ForeignKeyField, TextField, BigIntegerField
from playhouse.postgres_ext import ArrayField

from app import db


class BaseModel(Model):
    class Meta:
        database = db


class Mentor(BaseModel):
    id = AutoField(primary_key=True)
    first_name = TextField()
    last_name = TextField()
    email = TextField(index=True, unique=True)
    phone = BigIntegerField()
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

    class Meta:
        indexes = (
            (('first_name', 'last_name'), True),
        )


class Mentee(BaseModel):
    id = AutoField(primary_key=True)
    first_name = TextField()
    last_name = TextField()
    email = TextField(index=True)
    phone = BigIntegerField()
    created_on = DateTimeField(default=datetime.datetime.now)
    bio = TextField(null=True)
    academic_bio = TextField(null=True)
    job_search = TextField(null=True)
    technologies = ArrayField(field_class=TextField, null=True)
    years_experience = TextField(null=True)
    comments = TextField(null=True)

    class Meta:
        indexes = (
            (('first_name', 'last_name'), True),
        )


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


class Users(BaseModel):
    id = AutoField(primary_key=True)
    uid = TextField(null=True)
    created_on = DateTimeField(default=datetime.datetime.now, null=True)
    mentor_id = ForeignKeyField(Mentor, lazy_load=False, null=True)
    mentee_id = ForeignKeyField(Mentee, lazy_load=False, null=True)
    is_manager = BooleanField(default=False, null=True)
    is_admin = BooleanField(default=False, null=True)
