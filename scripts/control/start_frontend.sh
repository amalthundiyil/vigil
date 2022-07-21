#!/bin/bash

target=$1

FLASK_APP_PATH=$(realpath "sauron/backend/server")

if [[ $target == *"prod"* ]]; then
    echo "production"
else
    cd sauron/frontend && npm start
fi
