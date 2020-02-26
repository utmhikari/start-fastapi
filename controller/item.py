from service import item as item_service
from model.item import Item
from application.controller import success, error
from application.logger import get_controller_logger
from fastapi import APIRouter


router = APIRouter()
LOGGER = get_controller_logger('ITEM')


@router.get('/items/{item_id}')
def get_item(item_id: int):
    LOGGER.info('Get item with id: %d' % item_id)
    item = item_service.get_item(item_id)
    if not item:
        return error(msg='Cannot found item with id %d' % item_id)
    return success(item)


@router.put('/items/{item_id}')
def update_item(item_id: int, item: Item):
    LOGGER.info('Update item with id: %d' % item_id)
    ok = item_service.update_item(item_id, item)
    if not ok:
        return error(data=None, msg='Cannot found item with id %d' % item_id)
    return success(item)
