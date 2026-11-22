#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec daphne -b 0.0.0.0 -p 8000 simon_app.asgi:application
