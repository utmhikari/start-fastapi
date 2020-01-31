from service import item as item_service
from model.item import Item


def get_item(item_id: int) -> Item:
    return item_service.get_item(item_id)


def save_item(item_id: int, item: Item) -> Item:
    return item if item_service.save_item(item_id, item) else None
