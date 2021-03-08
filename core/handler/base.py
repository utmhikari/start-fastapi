from fastapi import APIRouter

from ..lib import logger
from ..model.handler import Resp

LOGGER = logger.for_handler('base')

ROUTER = APIRouter()


@ROUTER.get('/api/v1/core/health')
def health_check():
    """
    health check api
    :return: None
    """
    return Resp.ok(message='ok')
