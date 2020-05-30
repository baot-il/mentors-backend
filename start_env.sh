#!/bin/sh
export DATABASE_URL=postgresql://postgres:<your local db password>@localhost/postgres
export SECRET_KEY=someSecretStringUsedByFlask
export APP_SETTINGS=config.DevelopmentConfig
export FLASK_ENV=development
export GOOGLE_APPLICATION_CREDENTIALS=<path to secret key>

python reset_db.py
python main_app.py