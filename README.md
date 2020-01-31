# start-fastapi

a lightweight web server framework based on fastapi

基于[FastAPI](https://github.com/tiangolo/fastapi)的简易Web后端开发框架

简单组织了一下目录与数据结构，详细文档可以参考[FastAPI文档](https://fastapi.tiangolo.com/)

## Requirements

- python 3.6+ (for static typing check)
- pip3 install fastapi uvicorn

## Usage

run `start.sh` to start the dev server

whenever you write a router callback in a controller, remember to register it in main.py

## Structure

- controller: controller modules with router callbacks
- model: internal data models for typing check
- service: service libraries
- main.py: server entry
