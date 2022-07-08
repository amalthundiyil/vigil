#!/bin/bash
set -eo pipefail

scripts/install/checks.sh
if [[ $? -ne 0 ]]; then
  exit 1
fi

target=${1-prod}

if [[ $target == *"dev"* ]]; then
  echo
  echo "*****INSTALLING FOR DEVELOPMENT*****"
  echo
else
  echo
  echo "*****INSTALLING FOR PRODUCTION*****"
  echo
fi

scripts/install/backend.sh $target 2>&1 | tee logs/backend-install.log
echo "Done!"

if [[ ! -e sauron.config.json && ! -e $HOME/.sauron/sauron.config.json ]]; then
  echo "No config file found. Generating..."
  scripts/install/config.sh $target
else
  read -r -p "We noticed you have a config file already. Would you like to overwrite it with a new one? [Y/n] " response
  case "$response" in
      [yY][eE][sS]|[yY])
          echo "Generating a config file..."
          scripts/install/config.sh $target
          ;;
      *)
          ;;
  esac
fi

if [[ -e sauron.config.json || -e $HOME/.sauron/sauron.config.json ]]; then
  if [[ -e sauron.config.json ]]; then
    echo
    echo "*****NOTE THIS INSTANCES PORT USE AND CONFIGURATION EDITING INFORMATION*****"
    echo
    echo "These are the ports used in your configuration. The last two are your externally exposed API ports." 
    echo `cat sauron.config.json | grep -E port`
    echo "****************************************************************************"
    echo "You can edit these ports in the sauron.config.json file in this directory:"
    echo 
    echo `pwd`
    echo
    echo "****************************************************************************"
    echo
    echo "*****NOTE THIS INSTANCES PORT USE AND CONFIGURATION EDITING INFORMATION*****"
    echo
  else
    echo
    echo "*****NOTE THIS INSTANCES PORT USE AND CONFIGURATION EDITING INFORMATION*****"
    echo
    echo "These are the ports used in your configuration. The last two are your externally exposed API ports."
    echo `cat $HOME/.sauron/sauron.config.json | grep -E port`
    echo "****************************************************************************"
    echo "You can edit these ports in the sauron.config.json file in this directory:"
    echo 
    echo $HOME/.sauron/
    echo 
    echo "****************************************************************************"
    echo
    echo
    echo "*****NOTE THIS INSTANCES PORT USE AND CONFIGURATION EDITING INFORMATION*****"
    echo
  fi
fi

echo "**********************************"
echo "***** INSTALLATION COMPLETE *****"
echo "**********************************"
