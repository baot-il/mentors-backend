"""
Helper script to run migration operations on the PostgreSQL database.
Run locally, or remotely using Heroku's CLI
(heroku run python migrate.py --app <app_name>)
"""

from app import db
from playhouse.migrate import PostgresqlMigrator, migrate
from peewee import TextField


migrator = PostgresqlMigrator(db)
with db.atomic():
    migrate(
        # Mentor table
        migrator.add_column('mentor', 'first_name', TextField(index=True, null=True)),
        migrator.add_column('mentor', 'last_name', TextField(index=True, null=True)),
        migrator.drop_column('mentor', 'full_name'),
        
        # Mentee table
        migrator.add_column('mentee', 'first_name', TextField(index=True, null=True)),
        migrator.add_column('mentee', 'last_name', TextField(index=True, null=True)),
        migrator.drop_column('mentee', 'full_name'),
    )
