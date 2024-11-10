#!/bin/sh

# Realiza las migraciones
python manage.py migrate

# Si la variable de entorno 'DJANGO_ENV' es igual a 'local'
if [ "$DJANGO_ENV" = "local" ]; then
    echo "Iniciando en desarrollo con runserver..."
    python manage.py runserver 0.0.0.0:8000
else
  # Si no, usa gunicorn en produccion
  echo "Iniciando en producción con gunicorn..."
  gunicorn --bind 0.0.0.0:$PORT guardamelo_api.wsgi:application
fi