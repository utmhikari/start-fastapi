from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route, WebSocketRoute

from core import init_core_modules
from core.lib import cfg, util, logger

LOGGER = logger.get('FASTAPI_APP')


"""
FastAPI application main module
The APP instance will be launched by uvicorn instance in ${workspaceFolder}/main.py
"""


# init FastAPI instance with config integrated as environ vars
FASTAPI_CFG = {
    'debug': cfg.get('ENV') != 'prod',
    'title': cfg.get('TITLE'),
    'description': cfg.get('DESCRIPTION'),
    'version': cfg.get('VERSION'),
}
APP = FastAPI(**FASTAPI_CFG)


# register startup event
@APP.on_event('startup')
async def start_app():
    # init application
    LOGGER.info('launch fastapi application with cfg: %s' % util.pfmt(FASTAPI_CFG))
    # init core handlers, middlewares, events, etc
    init_core_modules(APP)
    # init handler routers
    from .handler import \
        test as test_handler
    # you can use your cfg to decide with routers should be loaded
    if FASTAPI_CFG.get('debug'):
        APP.include_router(test_handler.ROUTER)
    # dump routers
    LOGGER.info('routers are:')
    for route in APP.routes:
        if isinstance(route, Route):
            LOGGER.info('http router %s: %s %s' %
                        (route.name, route.path, route.methods))
        elif isinstance(route, WebSocketRoute):
            LOGGER.info('websocket router %s: %s ' %
                        (route.name, route.path))
    # middlewares
    APP.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    LOGGER.info('middlewares are:')
    for middleware in APP.user_middleware:
        LOGGER.info(repr(middleware))
    # services (currently only test service)
    from app.service import test
    test.init_market()


# register shutdown event
@APP.on_event('shutdown')
async def shutdown_app():
    LOGGER.info('shutdown fastapi application...')
