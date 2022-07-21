#!/bin/bash

target=$1

FLASK_APP_PATH=$(realpath "sauron/backend/server")

if [[ $target == *"prod"* ]]; then
    FLASK_ENV="production" python sauron/backend/app.py
else
    FLASK_ENV="development" python sauron/backend/app.py
fi

