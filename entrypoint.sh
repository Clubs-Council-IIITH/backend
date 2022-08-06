#!/usr/bin/env bash

# create/activate virtual environment
export VIRTUAL_ENV=.venv
python -m venv $VIRTUAL_ENV
export PATH="$VIRTUAL_ENV/bin:$PATH"

# install dependencies
pip install -r requirements.txt

# apply migrations & start django server
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runscript db_setup
python manage.py runserver 0.0.0.0:8000
