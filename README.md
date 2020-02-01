# start-fastapi

a lightweight web server framework based on fastapi

基于[FastAPI](https://github.com/tiangolo/fastapi)的简易Web后端开发框架

定位是快速实现效率工具/轻量级后端，比如xx机器人、xx数据处理服务器等，暂未有接一堆中间件SDK的计划

整个框架在fasiapi基础上梳理了目录结构、配置等容易踩坑的内容，这样业务就能基本专心写crud了

## Requirements

- python 3.6+ (for static typing check)
- pip3 install fastapi uvicorn

## Usage

### Run Example

the whole initial project is the example

cd to root dir and run `python3 ./main.py` to start the server

### 419
 
- add controller routes in `config/router.py` and write corresponding callbacks in `./controller`
- according to your controllers, write pylibs in `./service`
- write models in `./model` for services and controllers to enhance the robustness of code
- write middlewares if necessary
- if logging is needed, call `get_logger` func from `application.xxx` to get the logger
- cd to root dir and run `python3 ./main.py`

## Structure

- application: base apis for app modules (controllers, middlewares, services, etc)
- config: config files and scripts
- controller: controller modules with router callbacks
- middleware: middlewares
- model: internal data models for typing check
- service: service libraries
- main.py: server entry

## Customization

### Configuration

The main.py will do these tasks while initializing:

- load base application config on `config/app.json`
- load logging config on `config/logger.json` as uvicorn overwrites logging module
- register controller callbacks in `config/router.py`

so users should:

- confirm if needed controllers/middlwares are registered
- app is properly configured
- logger is properly configured

references on app and logger cfg:

- [uvicorn settings](https://www.uvicorn.org/settings/)
- [config.py](https://github.com/encode/uvicorn/blob/master/uvicorn/config.py)

### Miscs

- [FastAPI](https://fastapi.tiangolo.com/)
- [Starlette](https://www.starlette.io/)
- [Uvicorn](https://www.uvicorn.org/)

## TODO

- deployment
