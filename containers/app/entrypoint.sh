#!/bin/ash

set -e

python3 manage.py db_entrypoint
python3 manage.py collectstatic --noinput > /dev/null &

exec $@