#!/bin/bash

PS3="
Please type the number corresponding to your selection and then press the Enter/Return key.
Your choice: "

target=$1

if [[ ! -e sauron.config.json ]]; then
    touch ./sauron.config.json
else
    touch $HOME/.sauron/sauron.config.json 
fi
