# Setting up the database

1. Add CC Admin ID in `setup.py`.
2. Run:
```
python manage.py makemigrations
python manage.py migrate
python manage.py < setup.py
```
