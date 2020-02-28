from db import _get_technologies
from flask import Flask, request
from flask_cors import CORS, cross_origin
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CORS_HEADERS'] = 'Content-Type'
    cors = CORS(app)
    register_extensions(app)
    return app


def register_extensions(app):
    from extensions import db
    from extensions import migrate
    db.init_app(app)
    migrate.init_app(app)


app = create_app()


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/technologies', methods=['GET', 'POST'])
@cross_origin()
def get_technologies():
    return _get_technologies(request)


if __name__ == '__main__':
    app.run()
