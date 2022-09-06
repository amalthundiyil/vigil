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

echo "Installing ossf/scorecard"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  if [[ ! -f /usr/local/bin/scorecard ]]; then
    cd /usr/local/bin
    wget "https://github.com/ossf/scorecard/releases/download/v4.6.0/scorecard_4.6.0_linux_amd64.tar.gz"
    tar -xf scorecard_4.6.0_linux_amd64.tar.gz 
    mv scorecard-linux-amd64 scorecard
  fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
  if [[ ! -f /usr/local/bin/scorecard ]]; then
    cd /usr/local/bin
    wget "https://github.com/ossf/scorecard/releases/download/v4.6.0/scorecard_4.6.0_darwin_amd64.tar.gz"
    tar -xf scorecard_4.6.0_darwin_amd64.tar.gz 
    mv scorecard-darwin-amd64 scorecard
  fi
else
  echo "Couldn't recognize platform :/"
fi

echo "Completed installing ossf/scorecard"


echo "================================="
echo "===== INSTALLATION COMPLETE ====="
echo "================================="
