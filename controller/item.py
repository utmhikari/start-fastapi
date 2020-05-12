from service import item as item_service
from model.item import Item
from application.controller import success, error
from application.logger import get_controller_logger
from fastapi import APIRouter, BackgroundTasks


router = APIRouter()
LOGGER = get_controller_logger('ITEM')


@router.get('/item/{item_id}')
def get_item(item_id: int):
    """
    get item info by item id
    """
    LOGGER.info('Get item with id: %d' % item_id)
    item = item_service.get_item(item_id)
    if not item:
        return error(msg='Cannot found item with id %d' % item_id)
    return success(item)


@router.put('/item/{item_id}')
def update_item(item_id: int, item: Item):
    """
    update item info by item id
    """
    LOGGER.info('Update item with id: %d' % item_id)
    ok = item_service.update_item(item_id, item)
    if not ok:
        return error(data=None, msg='Cannot found item with id %d' % item_id)
    return success(item)


@router.get('/items/print')
def print_items(background_tasks: BackgroundTasks):
    """
    print item info in background
    """
    background_tasks.add_task(item_service.print_items_one_by_one, 1)
    return success(msg='Printing items now~')
