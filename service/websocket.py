from typing import Dict, Any
from application.logger import get_service_logger
from service import item as item_service

LOGGER = get_service_logger('WEBSOCKET')


def get_main_info() -> Dict[str, Any]:
    LOGGER.info('get websocket main info...')
    return {
        'name': 'fastapi_websocket',
        'tags': ['python', 'webapp']
    }


def get_item_info(item_id: int) -> Dict[str, Any]:
    LOGGER.info('get item info of id: %d' % item_id)
    item = item_service.get_item(item_id)
    return item.dict() if item else None
