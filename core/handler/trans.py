"""
Transaction handlers
"""
from fastapi import APIRouter

from ..lib import logger
from ..service import trans as trans_service

LOGGER = logger.for_handler('trans')
ROUTER = APIRouter()


@ROUTER.get('/api/v1/core/trans/handlers')
def get_trans_handlers():
    """
    get transaction handlers
    :return:
    """
    trans_manager = trans_service.get_manager()
    trans_manager.handlers
