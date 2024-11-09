#!/bin/sh
python manage.py migrate

gunicorn --bind 0.0.0.0:$PORT guardamelo_api.wsgi:application