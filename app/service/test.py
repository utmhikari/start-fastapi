import time
from typing import List, Optional

from app.model.test import Product, Customer, Market, MarketTransCode
from core.lib import logger
from core.model.base import ExecRet
from core.service import trans as trans_service

# logger
LOGGER = logger.for_service('test')

# test db
MARKET: Market = Market()
# products
PRODUCTS: List[Product] = [
    Product(pid=1, name='Maotai', origin='China', price=2000.0, num=10),
    Product(pid=2, name='NFC Juice', origin='China', price=7.0, num=2000),
    Product(pid=3, name='Oyakodon', origin='Japan', price=70.0, num=100),
    Product(pid=4, name='Lancome Genifique', origin='France', price=600.0, num=100),
    Product(pid=5, name='Tissue', origin='China', price=1.5, num=10000),
    Product(pid=6, name='Oyakodon', origin='China', price=40.0, num=500)
]
# customers
CUSTOMERS: List[Customer] = [
    Customer.male(cid=1, name='Adam', city='eden', balance=9999.9),
    Customer.female(cid=2, name='Eve', city='eden', balance=4567.3),
    Customer.male(cid=3, name='JackMa', city='hell', balance=1000000.0),
    Customer.male(cid=4, name='Benfen', city='toilet', balance=10.0),
    Customer.male(cid=5, name='Adam', city='washington', balance=1000.0)
]


def init_market() -> None:
    """
    init market data
    :return: None
    """
    LOGGER.info('initialize market data...')
    for product in PRODUCTS:
        MARKET.add_product(product)
    for customer in CUSTOMERS:
        MARKET.add_customer(customer)
    # register transactions
    trans_manager = trans_service.get_manager()
    trans_manager.register_handler(MarketTransCode.BUY_PRODUCT, buy_product)
    trans_manager.register_handler(MarketTransCode.MODIFY_PRICE, modify_price)


def get_market() -> Market:
    """
    get market instance
    :return: market instance
    """
    global MARKET
    if not isinstance(MARKET, Market):
        MARKET = Market()
        init_market()
    return MARKET


def get_customer_by_id(cid: int) -> Optional[Customer]:
    """
    get customer by id
    :param cid: customer id
    :return: customer instance
    """
    return get_market().get_customer(cid)


def get_product_by_id(pid: int) -> Optional[Product]:
    """
    get product by id
    :param pid: product id
    :return: product instance
    """
    return get_market().get_product(pid)


def get_customers_by_name(name: str = '') -> List[Customer]:
    """
    get customers by name
    :param name: customer name
    :return: list of customers with name
    """
    customers = []
    for c in get_market().customers.values():
        if not name or c.name == name:
            customers.append(c)
    return customers


def get_products_by_name(name: str = '') -> List[Product]:
    """
    get products by name
    :param name: product name
    :return: list of products with name
    """
    products = []
    for p in get_market().products.values():
        if not name or p.name == name:
            products.append(p)
    return products


def register_product(p: Product) -> ExecRet:
    """
    register a new product, pid should not exist
    :param p: product instance
    :return: if successfully added
    """
    market = get_market()
    pid = p.pid
    if pid in market.products.keys():
        return ExecRet.err(message='pid %d already exists' % pid)
    market.add_product(p)
    LOGGER.info('added product %s' % p.json())
    return ExecRet.ok()


"""
Transaction APIs
"""


def buy_product(pid: int, cid: int, num: int) -> ExecRet:
    """
    buy a product
    :param pid: product id
    :param cid: customer id
    :param num: product number
    :return: if successfully bought
    """
    market = get_market()
    time.sleep(3)
    ok, err = market.handle_transaction(cid, pid, num)
    LOGGER.info('handled transaction of pid: %d, cid: %d, num: %d --- %s, %s' %
                (pid, cid, num, str(ok), err))
    return ExecRet(success=ok, message=err)


def modify_price(pid: int, price: float) -> ExecRet:
    """
    modify price of a product
    :param pid: product id
    :param price: new price
    :return: if successfully modified
    """
    if price < 0.0:
        return ExecRet.err(message='invalid price %.4f' % price)
    market = get_market()
    product = market.get_product(pid)
    if not product:
        return ExecRet.err(message='pid %d not exist' % pid)
    LOGGER.info('pid %s, pre-price: %.4f, new-price: %.4f' %
                (pid, product.price, price))
    time.sleep(3)
    product.price = price
    return ExecRet.ok()
