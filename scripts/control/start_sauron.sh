#!/bin/bash

target=$1

FLASK_APP_PATH=$(realpath "sauron/backend/server")
MIGRATIONS_DIR="$FLASK_APP_PATH/models"

if [[ $target == *"prod"* ]]; then
    cd $MIGRATIONS_DIR && FLASK_APP=$FLASK_APP_PATH flask db migrate
    cd "../../../../"
    FLASK_ENV="production" python sauron/backend/app.py
else
    cd $MIGRATIONS_DIR && FLASK_APP=$FLASK_APP_PATH flask db migrate
    cd "../../../../"
    FLASK_ENV="development" python sauron/backend/app.py
fi

