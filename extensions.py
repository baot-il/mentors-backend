from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


migrate = Migrate()
db = SQLAlchemy()


def get_all_technologies():
    return
