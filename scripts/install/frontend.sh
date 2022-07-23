#!/bin/bash
set -eo pipefail

echo "Installing frontend dependencies..."
echo "=================================="
echo

target=$1

cd "sauron/frontend"
npm install
cd "../.."