from typing import Dict
from model.item import Item

__ITEMS: Dict[int, Item] = {
    1: Item(name='haha', price=1.1),
    22: Item(name='hehe', price=2.2),
    333: Item(name='gogo', price=3.3, is_offer=False),
}


def get_item(item_id: int) -> Item:
    return __ITEMS.get(item_id, None)


def save_item(item_id: int, item: Item) -> bool:
    __ITEMS[item_id] = item
    return True
