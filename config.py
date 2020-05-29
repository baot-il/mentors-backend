"""
Config file copied from this tutorial:
https://realpython.com/flask-by-example-part-1-project-setup/
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEVELOPMENT = True