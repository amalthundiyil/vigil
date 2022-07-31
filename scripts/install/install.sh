#!/bin/bash
set -eo pipefail

scripts/install/checks.sh
if [[ $? -ne 0 ]]; then
  exit 1
fi

target=${1-prod}

if [[ $target == *"dev"* ]]; then
  echo
  echo "======INSTALLING FOR DEVELOPMENT======"
  echo
else
  echo
  echo "======INSTALLING FOR PRODUCTION======="
  echo
fi

scripts/install/backend.sh $target 2>&1 | tee logs/backend-install.log
echo "Done!"
scripts/install/frontend.sh $target 2>&1 | tee logs/frontend-install.log
echo "Done!"

if [[ ! -e sauron.config.json && ! -e $HOME/.sauron/sauron.config.json ]]; then
  echo "No config file found. Generating..."
  scripts/install/config.sh $target
fi

echo "================================="
echo "===== INSTALLATION COMPLETE ====="
echo "================================="
