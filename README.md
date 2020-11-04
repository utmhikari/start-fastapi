# start-fastapi

Based on [FastAPI](https://github.com/tiangolo/fastapi), an easy-to-use web app developed upon [Starlette Framework](https://www.starlette.io/)

基于FastAPI的简易Web后端开发框架

定位是快速实现效率工具/轻量级后端，比如xx机器人、xx数据处理服务器等，暂未有接一堆中间件SDK的计划

整个框架在fastapi基础上梳理了目录结构、配置等容易踩坑的内容，这样业务就能基本专心写crud了

## Requirements

- python 3.6+ (for static typing check)
- `pip3 install -r ./requirements.txt` (recommended using venv)
- idea/pycharm (optional but recommended)

## Structure

非常经典的的洋葱圈模型

![onion](https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1604517336182&di=0f09d067f5e8512fbe22cb0373fab752&imgtype=0&src=http%3A%2F%2Fimg.shangdixinxi.com%2Fup%2Finfo%2F202001%2F20200130210409358062.png)

- application: base apis for web app modules
- build: build scripts
    - Dockerfile
- config
  - dev.cfg: app cfg of dev mode, using [python-dotenv](https://github.com/theskumar/python-dotenv)))
  - prod.cfg: app cfg of production mode
  - uvicorn: cfg for [uvicorn](https://www.uvicorn.org/settings/)
    - logger.json: [logging cfg](https://github.com/encode/uvicorn/blob/master/uvicorn/config.py) for uvicorn
    - dev.json: cfg for uvicorn launcher of dev mode
    - prod.json: cfg for uvicorn of prod mode
- controller: controller modules with router callbacks
- middleware: web app middlewares
- misc: misc items
  - script: user defined scripts
    - dev.sh: run app in dev mode
    - prod.sh: run app in prod mode
    - pack.sh: pack the web-app project
    - export.sh: dump requirements
    - test.sh: run test for routers
  - test: custom python scripts for testing modules
- model: internal data models for typing check
- service: service libraries
- app.py: fastapi application entry
- main.py: uvicorn entry

## Quick Start

### Launch App Server

Run script `./script/dev.sh(prod.sh)` or run command `./venv/bin(Scripts)/python main.py (dev/prod)` to start the server

To start the FastAPI app, [uvicorn ASGI server](https://www.uvicorn.org/) is needed. The steps are:

- uvicorn launches `app.py` with cfg in `config/uvicorn/dev(prod).json`
- `config/uvicorn/logger.json` will be the logger cfg for uvicorn
- app loads `config/dev(prod).cfg` as env config
- app registers controllers and middlewares, which launches the import of all modules

### Code Your Own Logic

- run server in dev mode, as hotfix is enabled
  - `./script/dev.sh`
  - `./venv/bin(Scripts)/python main.py dev`
- add controller routes in `config/router.py` and add corresponding callbacks in `./controller`
- add unique or multi-instance services in `./service` for your controllers
- add data models in `./model` for services and controllers
- add [middlewares](https://fastapi.tiangolo.com/tutorial/middleware/) if necessary
- GET `/docs` to test the routers on web page

### Handle Requests and Responses

All handled requests have status code of 200

If a request is not being successfully handled, users should call `error` in `application.controller` to wrap the response body

Otherwise, call `success` in `application.controller` to wrap the resp body

View [FastAPI Request Body](https://fastapi.tiangolo.com/tutorial/body/) for details

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

## Misc

### WebSocket

See `controller/websocket.py` for example, which took reference from [websocket documentation](https://fastapi.tiangolo.com/advanced/websockets/)
Websocket server holds the same port as http server's

### Export Dependencies

Run `pip freeze > requirements.txt` or `./script/export.sh` (if venv dir included) to export dependencies

### Testing

Testing for FastAPI is based on [pytest](https://docs.pytest.org/en/stable/)

See `./test/client.py` for script example, which took reference from fastapi docs:

- [testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [testing-websockets](https://fastapi.tiangolo.com/advanced/testing-websockets/)

Run `./script/test.sh ./test/client.py` to start your test

Using Postman or Insomnia is also recommended~

### Deployment

Run `./script/pack.sh` to pack the project into `./build/start-fastapi.tar.gz`

Take reference to `./build/Dockerfile` for [docker deployment](https://docs.docker.com/engine/reference/builder/)
