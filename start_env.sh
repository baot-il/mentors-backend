#!/bin/sh
export DATABASE_URL=postgresql://postgres:somePassword@localhost/postgres
export SECRET_KEY=someSecretStringUsedByFlask
export APP_SETTINGS=config.DevelopmentConfig
export GOOGLE_APPLICATION_CREDENTIALS=secretKey

python reset_db.py
python main_app.py
