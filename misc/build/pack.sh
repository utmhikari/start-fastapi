#!/usr/bin/env bash

ROOT_DIR=$(pwd)
TMP_DIR=./tmp
BUILD_PACK=misc/build/start-fastapi.tar.gz

# clean
rm -rf $TMP_DIR
mkdir -p $TMP_DIR
rm -f $BUILD_PACK

# clean __pycache__ and .pyc
cd "$ROOT_DIR" && find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

# copy files
cp -r ./app $TMP_DIR/app
cp -r ./cfg $TMP_DIR/cfg
cp -r ./core $TMP_DIR/core
cp -r ./misc $TMP_DIR/misc
cp ./main.py $TMP_DIR/main.py
cp ./requirements.txt $TMP_DIR/requirements.txt

# pack
cd $TMP_DIR && tar -cvf "$ROOT_DIR"/$BUILD_PACK ./*
cd "$ROOT_DIR" && rm -rf $TMP_DIR
