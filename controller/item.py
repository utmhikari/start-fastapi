from service import item as item_service
from model.item import Item
from application.controller import success, error
from application.logger import get_controller_logger
from fastapi import APIRouter, BackgroundTasks
from typing import Optional


router = APIRouter()
LOGGER = get_controller_logger('ITEM')


@router.get('/v1/item/{item_id}')
def get_item(item_id: int):
    """
    get item info by item id
    an example with param
    """
    LOGGER.info('Get item with id: %d' % item_id)
    item = item_service.get_item(item_id)
    if not item:
        return error(msg='Cannot found item with id %d' % item_id)
    return success(item)


@router.get('/v1/items')
def get_items(keyword: Optional[str] = '',
              min_price: Optional[float] = -1.0,
              max_price: Optional[float] = -1.0):
    """
    an example with query
    :return:
    """
    if 0 <= max_price < min_price:
        return error(msg='invalid price range!')
    items = item_service.get_items(keyword, min_price, max_price)
    return success(data=items)


@router.put('/v1/item/{item_id}')
def update_item(item_id: int, item: Item):
    """
    update item info by item id
    an example with body
    """
    LOGGER.info('Update item with id: %d' % item_id)
    ok = item_service.update_item(item_id, item)
    if not ok:
        return error(data=None, msg='Cannot found item with id %d' % item_id)
    return success(item)


@router.get('/v1/items/print')
def print_items(background_tasks: BackgroundTasks):
    """
    print item info in background
    an example with
    """
    background_tasks.add_task(item_service.print_items_one_by_one, 1)
    return success(msg='Printing items now~')
