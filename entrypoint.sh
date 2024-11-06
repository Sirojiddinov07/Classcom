#!/usr/bin/bash

python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input
python3 manage.py user
#poetry run gunicorn config.wsgi --reload --bind 0.0.0.0:8000 &
uvicorn config.asgi:application --port 8000 --host 0.0.0.0 &
celery -A config worker --loglevel=INFO

exit $?