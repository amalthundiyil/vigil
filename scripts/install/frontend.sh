#!/bin/bash
set -eo pipefail

echo "Installing frontend dependencies..."
echo "=================================="
echo

target=$1

cd "vigil/frontend"
npm install
cd "../.."