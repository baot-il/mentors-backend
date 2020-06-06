import os
from urllib.parse import uses_netloc, urlparse

from flask import Flask
from flask_cors import CORS
from peewee import PostgresqlDatabase, BigIntegerField
from playhouse.migrate import PostgresqlMigrator, migrate

uses_netloc.append('postgres')
url = urlparse(os.environ['DATABASE_URL'])

DATABASE = {
	'engine': 'peewee.PostgresqlDatabase',
	'name': url.path[1:],
	'password': url.password,
	'host': url.hostname,
	'port': url.port,
}

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = PostgresqlDatabase(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
)

# reference: https://peewee.readthedocs.io/en/latest/peewee/playhouse.html#schema-migrations
migrator = PostgresqlMigrator(db)
migrate(
	migrator.alter_column_type('mentee', 'phone', BigIntegerField()),
	migrator.alter_column_type('mentor', 'phone', BigIntegerField())
)
cors = CORS(app)

if __name__ == '__main__':
	app.run()
