#!/bin/bash

target=$1

if [[ $target == *"prod"* ]]; then
    FLASK_ENV="production" python sauron/backend/app.py
else
    FLASK_ENV="development" python sauron/backend/app.py
fi

