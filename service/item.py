from typing import Dict
from model import item as item_model

__ITEMS: Dict[int, item_model.Item] = {
    1: item_model.Item(name='haha', price=1.1),
    22: item_model.Item(name='hehe', price=2.2),
    333: item_model.Item(name='gogo', price=3.3, is_offer=False),
}


def get_item(item_id: int) -> item_model.Item:
    return __ITEMS.get(item_id, None)


def save_item(item_id: int, item: item_model.Item) -> bool:
    __ITEMS[item_id] = item
    return True
