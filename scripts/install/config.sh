#!/bin/bash

PS3="
Please type the number corresponding to your selection and then press the Enter/Return key.
Your choice: "

target=$1

if [[ ! -e vigil.config.json ]]; then
    touch ./vigil.config.json
else
    touch $HOME/.vigil/vigil.config.json 
fi