from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from models import Mentor, Mentee, Match, Technology


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/technologies')
def get_technologies():
    return {'technologies': ['Python', 'NodeJS', 'JavaScript', 'Machine Learning', 'TensorFlow']}


if __name__ == '__main__':
    app.run()
