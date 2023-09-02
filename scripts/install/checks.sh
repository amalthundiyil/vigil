#!/bin/bash

function check_python_version() {
  major_python_version=$($1 -c 'import sys; print(sys.version_info.major)')
  minor_python_version=$($1 -c 'import sys; print(sys.version_info.minor)')

  if [[ $major_python_version -lt 3 ]]; then
    echo "Outdated major version of Python detected."
    return 1
  elif [[ $minor_python_version -lt 6 ]]; then
    echo "Outdated minor version of Python detected."
    return 1
  fi
}

check_python_version "python"
if [[ $? -eq 1 ]]; then
  echo "Insufficient Python version installed to `which python`."
  echo "Checking `which python3`..."
  check_python_version "python3"
  if [[ $? -eq 1 ]]; then
    echo "Insufficient Python version installed to `which python3`."
    echo "Please install Python 3.6 or higher to either python or python3."
    echo "Python 3.6 and higher can be found here: https://www.python.org/downloads/"
    exit 1
  fi
fi

if [[ ! $(command -v pip) ]]; then
  echo "pip not found searching. Searching for pip3..."
  if [[ ! $(command -v pip3) ]]; then
    echo "Neither pip nor pip3 has been detected. Please make sure one of these two commands is installed and available in your PATH."
    echo "Installation instructions can be found here: https://pip.pypa.io/en/stable/installing/"
    exit 1
  fi
fi

if [[ ! -d logs ]]; then
    mkdir logs
fi

if [ ! -x "$(command -v docker)" ]; then
    echo "You need to install docker to run Vigil."
    exit 1
fi