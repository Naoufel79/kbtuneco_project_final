#!/usr/bin/env bash
set -o errexit
set -o nounset

python manage.py migrate --noinput
python manage.py ensure_superuser
python manage.py collectstatic --noinput

gunicorn kbtuneco.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers ${WEB_CONCURRENCY:-3} \
  --timeout ${GUNICORN_TIMEOUT:-120}

