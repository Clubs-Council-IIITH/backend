#!/usr/bin/env bash

# install dependencies
pip install -r requirements.txt

export DJANGO_SECRET_KEY=$(python SECRET_KEY.py)
export DJANGO_DEBUG=False

# collect all static files
python manage.py collectstatic --noinput

# Check Deployment Stats
python manage.py check --deploy

# apply migrations & serve using gunicorn
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runscript db_setup
gunicorn backend.wsgi --bind 0.0.0.0:8000
