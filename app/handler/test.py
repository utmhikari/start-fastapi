from typing import Dict, Any

from fastapi import APIRouter, UploadFile, File, WebSocket, BackgroundTasks
from starlette.websockets import WebSocketDisconnect

from app.model.test import MarketTransCode, Product
from app.service import test as test_service
from core.lib import util, logger
from core.model.handler import Resp
from core.service import trans as trans_service

LOGGER = logger.for_handler('test')

ROUTER = APIRouter()


@ROUTER.get('/api/v1/test/products/{pid}')
def get_product_by_id(pid: int):
    """
    get product by id
    :param pid: product id
    :return: product
    """
    product = test_service.get_product_by_id(pid)
    if not product:
        return Resp.err(message='cannot get product by id %d' % pid)
    return Resp.ok(data=product.dict())


@ROUTER.get('/api/v1/test/products')
def get_products_by_name(name: str = ''):
    """
    get products by name
    A QUERY EXAMPLE
    :param name: product name
    :return: product list
    """
    products = test_service.get_products_by_name(name)
    return Resp.ok(data=[p.dict() for p in products])


@ROUTER.get('/api/v1/test/customers/{cid}')
def get_customer_by_id(cid: int):
    """
    get customer by id
    :param cid: customer id
    :return: customer
    """
    customer = test_service.get_customer_by_id(cid)
    if not customer:
        return Resp.err(message='cannot get customer by id %d' % cid)
    return Resp.ok(data=customer.dict())


@ROUTER.get('/api/v1/test/customers')
def get_customers_by_name(name: str = ''):
    """
    get customers by name
    :param name: customer name
    :return: customer list
    """
    customers = test_service.get_customers_by_name(name)
    return Resp.ok(data=[p.dict() for p in customers])


@ROUTER.post('/api/v1/test/products')
def register_product(product: Product):
    """
    register product
    :param product: Product body
    :return: None
    """
    ret = test_service.register_product(product)
    if not ret.success:
        return Resp.err(message=ret.message)
    return Resp.ok()


@ROUTER.get('/api/v1/test/products/{pid}/buy')
def buy_product(pid: int, cid: int, num: int, background_tasks: BackgroundTasks):
    """
    buy a product
    :param pid: product id
    :param cid: customer id
    :param num: product num
    :param background_tasks: bg context
    :return: None
    """
    trans_manager = trans_service.get_manager()
    background_tasks.add_task(trans_manager.call, MarketTransCode.BUY_PRODUCT, pid, cid, num)
    return Resp.ok(message='invoked buy product transaction')


@ROUTER.put('/api/v1/test/products/{pid}/price')
def modify_price(pid: int, body: Dict[str, Any], background_tasks: BackgroundTasks):
    """
    modify price of a product
    :param pid: product id
    :param body: body
    :param background_tasks: bg context
    :return: None
    """
    price, err = util.as_float(body.get('price'))
    if err is not None:
        return Resp.err(message=str(err))
    trans_manager = trans_service.get_manager()
    background_tasks.add_task(trans_manager.call, MarketTransCode.MODIFY_PRICE, pid, price)
    return Resp.ok(message='invoked modify price transaction')


@ROUTER.post('/api/v1/test/upload')
async def upload_file(file: UploadFile = File(...)):
    """
    an example of uploading file
    :param file: file instance
    :return: file info
    """
    filename = file.filename
    content = await file.read()
    decoded_content = content.decode(util.ENCODING)
    LOGGER.info('Received file %s:\n%s' % (
        filename,
        decoded_content
    ))
    return Resp.ok(data={
        'filename': filename,
        'contentType': file.content_type,
        'size': len(decoded_content)
    })


@ROUTER.websocket('/api/v1/test/health')
async def health_check(websocket: WebSocket):
    """
    websocket health check
    :param websocket: websocket instance
    :return: None
    """
    await websocket.accept()
    await websocket.send_json(Resp.ok(message='hello world'))
    await websocket.close()


@ROUTER.websocket('/api/v1/test/customer')
async def get_customer_info(websocket: WebSocket):
    """
    a tunnel to get customer info
    :param websocket: ws instance
    :return: None
    """
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            if not data.isdigit():
                await websocket.send_json(Resp.err(message='customer id should be digit!'))
                continue
            customer = test_service.get_customer_by_id(int(data))
            if not customer:
                await websocket.send_json(Resp.err(message='cannot find customer'))
            else:
                await websocket.send_json(Resp.ok(data=customer.dict()))
        except WebSocketDisconnect:
            LOGGER.info('websocket of customer disconnected!')
            break
        except Exception as e:
            LOGGER.exception('websocket of customer encountered an exception: %s' % e)
            break
