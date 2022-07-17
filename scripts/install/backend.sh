#!/bin/bash
set -eo pipefail

echo "Installing backend dependencies..."
echo "**********************************"
echo

target=$1

if [[ $target == *"prod"* ]]; then
    pip install .
else
    pip install -e .[dev]
fi

APP_PATH=$(realpath "sauron/backend")

if [[ ! -d $APP_PATH/migrations ]]; then
    cd $APP_PATH && flask db init && flask db migrate
fi