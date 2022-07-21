#!/bin/bash
set -eo pipefail

echo "Installing backend dependencies..."
echo "=================================="
echo

target=$1

if [[ $target == *"prod"* ]]; then
    pip install .
else
    pip install -e .'[dev]'
fi

# FLASK_APP_PATH=$(realpath "sauron/backend/server")
# MIGRATIONS_DIR="$FLASK_APP_PATH/models"

# if [[ ! -d "$MIGRATIONS_DIR/migrations" ]]; then
#     cd $MIGRATIONS_DIR && FLASK_APP=$FLASK_APP_PATH flask db init 
#     cd $MIGRATIONS_DIR && FLASK_APP=$FLASK_APP_PATH flask db migrate
# fi