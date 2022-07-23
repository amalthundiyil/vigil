#!/bin/bash
set -eo pipefail

echo "Installing frontend dependencies..."
echo "=================================="
echo

target=$1

cd "sauron/frontend"
# if [ $GITHUB_ACTIONS ]; then
#     npm ci 
# else
    npm install
# fi

cd "../.."