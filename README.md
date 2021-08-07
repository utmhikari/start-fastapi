# start-fastapi

Version 2021, based on [FastAPI](https://github.com/tiangolo/fastapi), an easy-to-use web app developed upon [Starlette Framework](https://www.starlette.io/)

- [Version 2020](https://github.com/utmhikari/start-fastapi/tree/v2020_final)
- [中文文档](./misc/doc/README_CN.md)

## Requirements

- python 3.6+ (for static typing check)
- `pip3 install -r ./requirements.txt`
  - fastapi, uvicorn, python-dotenv, python-multipart, websockets, etc
- idea/pycharm (recommended) + venv

## Structure

The web application is based on onion style~

![onion](http://www.zyiz.net/upload/202006/15/202006150525428099.png)

The directory structure is:

- app: logics for your application, includes `__init__.py` as entry of user modules
  - handler: controllers
  - middleware: router middleware, like cors
  - model: basic data models and internal logics
  - service: external logics (to users)
- cfg: config of different envs
  - dev: configs of dev env
    - app.cfg: [python-dotenv](https://github.com/theskumar/python-dotenv) cfg for fastapi
    - uvicorn.json: cfg for [uvicorn ASGI server](https://www.uvicorn.org/), the launcher for fastapi
    - logger.json: [logging cfg](https://github.com/encode/uvicorn/blob/master/uvicorn/config.py) for uvicorn
  - prod: configs of production env
- core: low level libraries and logics, includes `__init__.py` as entry of core modules, better make it able to be reused in other projects
  - handler
  - lib: shortcut apis for user to build logics
  - model
  - service
    - trans: **transaction service**, for managing tasks running in background
- misc: misc parts, like build, test scripts, etc
  - build: build scripts
  - dev: resources for dev usage
    - gen_code.py: a script for generating codes
  - doc: docs
  - test: test scripts
- main.py: main entry, init uvicorn and start fastapi app
- requirements.txt: py package requirements

## Quick Start

### Launch App Server

Run `./main.py` to start the example, which includes:

- core modules: health check handler, basic models, transaction service
- [cors](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) middleware configured with wildcard *
- test handlers, models and service: simulates a simple market trade system with products and customers
  - examples of websocket and upload file are also included in test handlers

The internal steps are:

- `./main.py` loads the configs inside `./cfg/{env}` on cmd args, then calls `uvicorn.run` to start fastapi app at `./app/__init__.py`
- in `./app/__init__.py`, core modules and user handlers/models/services are loaded at `startup` event of fastapi app

You can put your launch scripts inside `./misc/build` for your different launch options

### Coding Guide

To build your logic, common steps are follows:

- `./main.py` runs server in dev environment in default, in which hot-reload is enabled
- add handlers in `./app/handler`, add corresponding `import` & `APP.include_router` codes in `./app/__init__.py`
- add data models in `./app/model`, add services in `./app/service`
- add [middlewares](https://fastapi.tiangolo.com/tutorial/middleware/) in `./app/middleware` if necessary

Some tips for coding:

- GET `/docs` to test the routers on web page
- Avoid using coroutines (`async def` functions), as it may block the main evtloop, so that other requests are not handled in time. `def` functions will be invoked in different threads
- codes of `./core` should be shareable (for other projects), codes of `./app` should fit with current project
- You can use `./misc/dev/gen_code.py` to generate template codes for handlers, models & services. Exec it with working directory as project root directory
- Code models based on `pydantic.BaseModel`, it's powerful

### HTTP Response

Most of the handled requests should contain a status code of 200

A simple solution is to use `Resp` model in `./core/model/handler.py` to generate response body for your handlers

```text
{
  "success": bool,
  "message": str,
  "code": IntEnum,
  "data": Any,
}
```

Use `Resp.ok` to generate success response and use `Resp.err` to generate error response

## Misc

### WebSocket

The test handler `./app/handler/test.py` contains ws handler examples

To know more about it, see [websocket documentation](https://fastapi.tiangolo.com/advanced/websockets/)

### Deployment

Run `./misc/build/pack.sh` to pack the project into `./misc/build/start-fastapi.tar.gz`

See `./misc/build/Dockerfile` for an example of [docker deployment](https://docs.docker.com/engine/reference/builder/)
