from typing import Dict
from model.item import Item
from application.service import get_logger

LOGGER = get_logger('ITEM')

_ITEMS: Dict[int, Item] = {
    1: Item(name='haha', price=1.1),
    22: Item(name='hehe', price=2.2),
    333: Item(name='gogo', price=3.3, is_offer=False),
}


def get_item(item_id: int) -> Item:
    return _ITEMS.get(item_id, None)


def update_item(item_id: int, item: Item) -> bool:
    if item_id in _ITEMS.keys():
        _ITEMS[item_id] = item
        return True
    return False
