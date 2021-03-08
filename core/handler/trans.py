"""
Transaction handlers
"""
from fastapi import APIRouter

from ..lib import logger
from ..service import trans as trans_service
from ..model.handler import Resp

LOGGER = logger.for_handler('trans')
ROUTER = APIRouter()


@ROUTER.get('/api/v1/core/trans/handlers')
def get_trans_handlers():
    """
    get transaction handlers
    :return:
    """
    trans_manager = trans_service.get_manager()
    handlers = {}
    for code, handler in trans_manager.handlers.items():
        handlers[code.value] = str(handler.__name__)
    return Resp.ok(data=handlers)
