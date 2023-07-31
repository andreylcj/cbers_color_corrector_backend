#!/bin/bash

docker run \
    --env-file "$(pwd)/.env" \
    -v "$(pwd)/src/cbers_cc:/home/cbers_cc/src/cbers_cc" \
    cbers_cc_backend_django \
    bash -c "cd src/cbers_cc/; python manage.py migrate"