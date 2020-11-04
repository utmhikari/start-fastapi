from fastapi import FastAPI
from application import router, config, logger
from application.util import pfmt
from typing import Dict, Any
from starlette.routing import Route, WebSocketRoute

"""
USE os.getenv() TO GET ENV VARS IN dev.cfg OR prod.cfg
"""

env: str = config.get('ENV')
app_name: str = config.get('APP_NAME')
description: str = config.get('DESCRIPTION')
version: str = config.get('VERSION')
debug: bool = config.get_bool('DEBUG')

fastapi_cfg: Dict[str, Any] = {
    'debug': env != 'prod',
    'title': app_name,
    'description': description,
    'version': version,
    'is_debug': debug
}

# init app
app = FastAPI(**fastapi_cfg)
router.register_controllers(app)
router.register_middlewares(app)

LOGGER = logger.get_application_logger()


@app.on_event('startup')
async def start_app():
    LOGGER.info('Launching application: %s\n%s' % (app_name, pfmt(fastapi_cfg)))
    # dump routers
    LOGGER.info('ROUTERS:')
    for route in app.routes:
        if isinstance(route, Route):
            LOGGER.info('HTTP Router %s: %s %s' %
                        (route.name, route.path, route.methods))
        elif isinstance(route, WebSocketRoute):
            LOGGER.info('WebSocket Router %s: %s ' %
                        (route.name, route.path))
    # dump user middlewares
    LOGGER.info('USER MIDDLEWARES:')
    for user_middleware in app.user_middleware:
        LOGGER.info(repr(user_middleware))


@app.on_event('shutdown')
async def shutdown_app():
    LOGGER.info('Shutdown application~')
