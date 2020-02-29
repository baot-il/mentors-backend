from flask import Flask
from flask_cors import CORS
from peewee import PostgresqlDatabase
from urllib.parse import uses_netloc, urlparse
import os

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
db = PostgresqlDatabase(database=url.path[1:],
                        user=url.username,
                        password=url.password,
                        host=url.hostname,
                        port=url.port)
cors = CORS(app)


if __name__ == '__main__':
    app.run()
