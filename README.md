# start-fastapi

a lightweight web server framework based on fastapi

基于[FastAPI](https://github.com/tiangolo/fastapi)的简易Web后端开发框架

定位是快速实现效率工具/轻量级后端，比如xx机器人、xx数据处理服务器等，暂未有接一堆中间件SDK的计划

整个框架在fasiapi基础上梳理了目录结构、配置等容易踩坑的内容，这样业务就能基本专心写crud了

## References

一般的文档在这3个地方找就ok了

- [FastAPI](https://fastapi.tiangolo.com/)
- [Starlette](https://www.starlette.io/)
- [Uvicorn](https://www.uvicorn.org/)

## Requirements

- python 3.6+ (for static typing check)
- `pip3 install -r ./requirements.txt` (using venv is recommended)
- idea/pycharm (optional but recommended)

## Structure

非常经典的的洋葱圈模型

- application: base apis for app modules (config, logger, router, etc)
- build: build scripts like Dockerfile
- config: config files (json and python dotenv)
- controller: controller modules with router callbacks
- middleware: middlewares
- model: internal data models for typing check
- script: user defined scripts
- service: service libraries
- test: custom python scripts for testing modules
- util: util libraries
- app.py: fastapi application entry
- main.py: uvicorn entry

## Configuration

First let's see steps of initializing application:

- user runs command `./venv/bin(Scripts)/python main.py (dev/prod)`
- uvicorn launches `app.py` with cfg in `config/uvicorn/dev(prod).json`
- `config/uvicorn/logger.json` will be the logger cfg for uvicorn
- app loads `config/dev(prod).cfg` as env config
- app registers controllers and middlewares, which launches the import of all modules

so we needed such references:

references on configuring app and logger json:

- [uvicorn settings](https://www.uvicorn.org/settings/)
- [config.py](https://github.com/encode/uvicorn/blob/master/uvicorn/config.py)

references on configuring dev.cfg or prod.cfg:

- [python-dotenv](https://github.com/theskumar/python-dotenv)

## Example

the whole initial project is the example, cd to root dir and run `./script/dev.sh` to start the server

if you want to code your own logic then:

- add controller routes in `config/router.py` and add corresponding callbacks in `./controller`
- according to your controllers, add unique or multi-instance services in `./service`
- add data models in `./model` for services and controllers
- add middlewares if necessary, see [fastapi middleware](https://fastapi.tiangolo.com/tutorial/middleware/)
- if logging is needed, call `get_logger` func from `application.xxx` to get the logger
- cd to root dir and run `python3 ./main.py`

全局性质的对象尽可能放到application中，unique service跟多实例的service都放到service下，后者用class封装就好了

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

所有能处理走到逻辑的都返回200，由success和code控制处理结果。不能处理或处理出exception的，由fastapi底层代理

### export your requirements

while working collaboratively, each member should synchronize the libraries if needed

run `pip freeze > requirements.txt` or `./script/export.sh` (if venv dir included) before commit

## Deployment

run `./script/pack.sh` to pack the project into `./build/start-fastapi.tar.gz`

if docker deployment is needed, take reference to `./build/Dockerfile`

## TODO

- testing
- RBAC
