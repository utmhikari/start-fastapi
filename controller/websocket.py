from fastapi import WebSocket, APIRouter
from service import websocket as websocket_service
from application import logger
from application.controller import success, error


LOGGER = logger.get_controller_logger('WEBSOCKET')

router = APIRouter()


@router.websocket('/v1/health')
async def health_check(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json(success(msg='hello world'))
    await websocket.close()


@router.websocket('/v1/items')
async def get_item_info(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        if not data.isdigit():
            await websocket.send_json(error(msg='item id should be digit!'))
            continue
        item_id = int(data)
        item_info = websocket_service.get_item_info(item_id)
        if not item_info:
            await websocket.send_json(error(msg='cannot find item info'))
        await websocket.send_json(success(item_info))
