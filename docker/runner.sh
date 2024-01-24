#!/bin/sh

set -o allexport
. docker/.env
set +o allexport

python3 manage.py migrate
python3 manage.py runscript populate-db

exec $@

