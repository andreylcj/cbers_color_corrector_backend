#!/bin/bash

app_name="$1"

echo "!********************************************************!"
echo "!*** [START] Test ***!"
echo "!********************************************************!"

if [ -z "$app_name" ]; then
    docker run \
        --env-file "$(pwd)/.env" \
        -v "$(pwd)/src/cbers_cc:/home/cbers_cc/src/cbers_cc" \
        cbers_cc_backend_django \
        bash -c "cd src/cbers_cc/; python manage.py test --noinput"
else
    docker run \
        --env-file "$(pwd)/.env" \
        -v "$(pwd)/src/cbers_cc:/home/cbers_cc/src/cbers_cc" \
        cbers_cc_backend_django \
        bash -c "cd src/cbers_cc/; python manage.py test $app_name --noinput"
fi


if [ $? = 0 ]; then
    echo "!********************************************************!"
    echo "!*** [END] Test Success ***!"
    echo "!********************************************************!"
    exit 0
else
    echo "!********************************************************!"
    echo "!*** [END] Test Fail ***!"
    echo "!********************************************************!"
    exit 1
fi