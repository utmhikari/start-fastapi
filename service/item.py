from typing import Dict, List
from model.item import Item
from application.logger import get_service_logger
import time, pprint

LOGGER = get_service_logger('ITEM')

_ITEMS: Dict[int, Item] = {
    1: Item(name='haha', price=1.1),
    22: Item(name='hehe', price=2.2),
    333: Item(name='gogo', price=3.3, is_offer=False),
    99: Item(name='ronaldo', price=10000.00, is_offer=False)
}


def get_item(item_id: int) -> Item:
    return _ITEMS.get(item_id, None)


def get_items(keyword: str = '',
              min_price: float = -1.0,
              max_price: float = -1.0) -> List[Item]:
    items = []
    for _, item in _ITEMS.items():
        if keyword and keyword not in item.name:
            continue
        if min_price > 0.0 and min_price > item.price:
            continue
        if 0.0 < max_price < item.price:
            continue
        items.append(item)
    return items


def update_item(item_id: int, item: Item) -> bool:
    if item_id not in _ITEMS.keys():
        return False
    _ITEMS[item_id] = item
    return True


def print_items_one_by_one(interval: int = 3):
    if interval <= 0:
        interval = 3
    for item_id, item_info in _ITEMS.items():
        LOGGER.info('Item %d: %s' % (item_id, pprint.pformat(item_info)))
        time.sleep(interval)
    LOGGER.info('Finish printing items!')
