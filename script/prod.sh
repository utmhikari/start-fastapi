#!/usr/bin/env bash

BIN_DIR=./venv/Scripts

if [ ! -d "$BIN_DIR" ]; then
  BIN_DIR=./venv/bin
fi

$BIN_DIR/python main.py -e prod