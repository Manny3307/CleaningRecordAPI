#!/bin/sh
cd app
sudo python manage.py migrate --no-input
sudo python manage.py collectstatic --no-input

gunicorn app.wsgi:application --bind 0.0.0.0:8000