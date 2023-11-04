#!/bin/bash

clean_python_caches() {
  find . -type d -name "__pycache__" -exec rm -r {} +
}

clean_venvs() {
  find . -type d -name "venv" -exec rm -r {} +
}

clean_builds() {
  find . -type d -name "*.egg-info" -exec rm -r {} +
  find . -type d -name "*.dist" -exec rm -r {} +
  find . -type d -name "dist" -exec rm -r {} +
  find . -type d -name "build" -exec rm -r {} +
}

clean_frontend() {
  find . -name 'node_modules' -type d -prune -exec rm -rf '{}' +
}


clean_python_caches
clean_venvs
clean_builds
clean_frontend

echo "Clean completed."
