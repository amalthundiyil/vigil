#!/bin/bash

bash scripts/clean.sh
bash scripts/env.sh

okteto context use https://cloud.okteto.com --token $OKTETO_TOKEN
okteto deploy -n amalthundiyil

cd vigil/frontend
vercel deploy
cd ../..
