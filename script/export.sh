#!/usr/bin/env bash

BIN_DIR=./venv/Scripts

if [ ! -d "$BIN_DIR" ]; then
  BIN_DIR=./venv/bin
fi

rm -f ./requirements.txt
$BIN_DIR/pip freeze > ./requirements.txt
