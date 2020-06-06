#!/bin/sh
source .env

python reset_db.py
python main_app.py
