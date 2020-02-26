# start-fastapi

a lightweight web server framework based on fastapi

基于[FastAPI](https://github.com/tiangolo/fastapi)的简易Web后端开发框架

定位是快速实现效率工具/轻量级后端，比如xx机器人、xx数据处理服务器等，暂未有接一堆中间件SDK的计划

整个框架在fasiapi基础上梳理了目录结构、配置等容易踩坑的内容，这样业务就能基本专心写crud了

## References

- [FastAPI](https://fastapi.tiangolo.com/)
- [Starlette](https://www.starlette.io/)
- [Uvicorn](https://www.uvicorn.org/)

## Requirements

- python 3.6+ (for static typing check)
- pip3 install -r ./requirements.txt (using venv is recommended)

## Structure

- application: base apis for app modules (controllers, middlewares, services, router, etc)
- config: config files (json)
- controller: controller modules with router callbacks
- middleware: middlewares
- model: internal data models for typing check
- service: service libraries
- test: custom test scripts
- main.py: server entry

## Tutorial

### Example

the whole initial project is the example, cd to root dir and run `./script/dev.sh` to start the server

if you want to code your own logic then:

- add controller routes in `config/router.py` and write corresponding callbacks in `./controller`
- according to your controllers, write pylibs in `./service`
- write models in `./model` for services and controllers to enhance the robustness of code
- write middlewares if necessary
- if logging is needed, call `get_logger` func from `application.xxx` to get the logger
- cd to root dir and run `python3 ./main.py`

### Requests and Responses

all handled requests have status code of 200

if a request is not successfully handled, users should call `error` in `application.controller` to wrap the response body

otherwise, call `success` in `application.controller` to wrap the resp body

The request body schema is defined on user, view [FastAPI Request Body](https://fastapi.tiangolo.com/tutorial/body/) for details

The base schema of response body is:

```text
{
  "success": bool,
  "message": string,
  "code": int,
  "data": any,
}
```

### export your requirements

while working collaboratively, each member should synchronize the libraries if needed

run `pip freeze > requirements.txt` or `./script/export.sh` (if venv dir included) before commit

## Customization

### Configuration

The main.py will do these tasks while initializing:

- load base application config on `config/dev.cfg` or `config/prod.json` based on `-e` arg to `main.py`
  - for example, run `python3 main.py -e prod`, will run app using `prod.json`
- the `config/dev.json` or `config/prod.json` will hold an option on logger config path, so that `config/logger/logger.json` will overwrite uvicorn logging config
- register controller callbacks in `config/router.py`

so users should:

- confirm if needed controllers/middlwares are registered
- app is properly configured
- logger is properly configured

references on app and logger cfg:

- [uvicorn settings](https://www.uvicorn.org/settings/)
- [config.py](https://github.com/encode/uvicorn/blob/master/uvicorn/config.py)

## TODO

- deployment
- error handle
