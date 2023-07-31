#!/bin/bash

app_name="$1"

if [ -z "$app_name" ]; then
    docker run \
        --env-file "$(pwd)/.env" \
        -v "$(pwd)/src/cbers_cc:/home/cbers_cc/src/cbers_cc" \
        cbers_cc_backend_django \
        bash -c "cd src/cbers_cc/; python manage.py makemigrations"
else
    docker run \
        --env-file "$(pwd)/.env" \
        -v "$(pwd)/src/cbers_cc:/home/cbers_cc/src/cbers_cc" \
        cbers_cc_backend_django \
        bash -c "cd src/cbers_cc/; python manage.py makemigrations $app_name"
fi