#!/usr/bin/env bash

# install dependencies
pip install -r requirements.txt

# collect all static files
python manage.py collectstatic --noinput

# apply migrations & serve using gunicorn
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runscript db_setup
gunicorn backend.wsgi --bind 0.0.0.0:8000
