from controller import base, item
from middleware import connection
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def register_controllers(app: FastAPI) -> None:
    """
    register controller callbacks to routers
    NOTE: /docs & /redoc are internal routers of fastapi
    :param app: fastapi app
    :return: None
    """
    app.get('/')(base.get_root)
    app.get('/items/{item_id}')(item.get_item)
    app.put('/items/{item_id}')(item.update_item)


def register_middlewares(app: FastAPI) -> None:
    """
    register middlewares
    :param app: fastapi app
    :return: None
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.middleware('http')(connection.calc_time)
