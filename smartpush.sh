#!/bin/bash

commit_message=$1

if [ -z "$commit_message" ]; then
    message="Default commit"
fi

git add .
git commit -m "$message"
git push