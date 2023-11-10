#!/bin/bash

set -m
cd /opt/lexicom/app || { echo "No such directory"; exit 1; }
/opt/poetry/bin/poetry run uvicorn --reload --host=0.0.0.0 --port=8000 main:app
