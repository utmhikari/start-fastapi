"""
Core module initialization
"""
from fastapi import FastAPI

from .handler import \
    base, \
    trans as trans_handler


def init_core_modules(app: FastAPI) -> None:
    """
    Init core handlers, middlewares and services for fastapi application
    :return: None
    """
    # handlers
    app.include_router(base.ROUTER)
    app.include_router(trans_handler.ROUTER)
    # services
    from core.service import \
        trans as trans_service
