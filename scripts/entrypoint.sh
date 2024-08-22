#!/usr/bin/bash

poetry run python3 manage.py migrate --no-input
poetry run python3 manage.py collectstatic --no-input
#poetry run gunicorn config.wsgi --reload --bind 0.0.0.0:8000 &
poetry run daphne -p 8000 -b 0.0.0.0 config.asgi:application &
poetry run celery -A config worker -l info

exit $?