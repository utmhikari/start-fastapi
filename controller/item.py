from service import item as item_service
from model import item as item_model


def get_item(item_id: int) -> item_model.Item:
    return item_service.get_item(item_id)


def save_item(item_id: int, item: item_model.Item) -> item_model.Item:
    return item if item_service.save_item(item_id, item) else None
