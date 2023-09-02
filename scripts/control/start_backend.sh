#!/bin/bash

target=$1

FLASK_APP_PATH=$(realpath "vigil/backend/server")

if [[ $target == *"prod"* ]]; then
    FLASK_ENV="production" python vigil/backend/app.py
else
    FLASK_ENV="development" python vigil/backend/app.py
fi

