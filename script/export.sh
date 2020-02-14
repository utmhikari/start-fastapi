#!/usr/bin/env bash

rm -f ./requirements.txt
./venv/Scripts/pip freeze > ./requirements.txt
