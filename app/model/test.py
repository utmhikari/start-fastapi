from enum import IntEnum
from typing import Dict, Optional

from pydantic import BaseModel

from core.model.base import PCallRet


class MarketTransCode(IntEnum):
    """
    market transaction codes
    """
    BUY_PRODUCT = 1001
    MODIFY_PRICE = 1002


class Product(BaseModel):
    """
    product model
    """
    pid: int
    name: str
    origin: str
    price: float
    num: int = 0
    profit: float = 0.0


class Sex(IntEnum):
    """
    sex enum
    """
    FEMALE = 0
    MALE = 1


class Customer(BaseModel):
    """
    customer model
    """
    cid: int
    name: str
    sex: Sex
    city: str = ''
    balance: float = 0.0
    products: Dict[int, int] = {}  # { pid: num }

    @classmethod
    def female(cls, **kwargs):
        return Customer(sex=Sex.FEMALE, **kwargs)

    @classmethod
    def male(cls, **kwargs):
        return Customer(sex=Sex.MALE, **kwargs)


class Market(BaseModel):
    """
    market instance
    """
    products: Dict[int, Product] = {}
    customers: Dict[int, Customer] = {}

    def add_product(self, product: Product) -> None:
        """
        add a product
        :param product: product instance
        :return: None
        """
        assert product.pid not in self.products.keys()
        self.products[product.pid] = product

    def add_customer(self, customer: Customer) -> None:
        """
        add a customer
        :param customer: customer instance
        :return: None
        """
        assert customer.cid not in self.customers.keys()
        self.customers[customer.cid] = customer

    def get_product(self, pid: int) -> Optional[Product]:
        """
        get product by pid
        :param pid: product id
        :return: optional product instance
        """
        return self.products.get(pid)

    def get_customer(self, cid: int) -> Optional[Customer]:
        """
        get customer by cid
        :param cid: customer id
        :return: optional customer instance
        """
        return self.customers.get(cid)

    def handle_transaction(self, cid: int, pid: int, num: int) -> PCallRet:
        """
        handle transaction
        :param cid: customer id
        :param pid: product id
        :param num: number of products
        :return: ok (if transaction is successful), err (error message)
        """
        if num <= 0:
            return False, 'invalid trade num %d' % num
        customer = self.get_customer(cid)
        if not customer:
            return False, 'no customer with id %d' % cid
        product = self.get_product(pid)
        if not product:
            return False, 'no product with id %d' % pid
        if product.num < num:
            return False, 'insufficient products'
        exchange = product.price * num
        if customer.balance < exchange:
            return False, 'insufficient balance'
        if pid not in customer.products.keys():
            customer.products[pid] = 0
        customer.products[pid] += num
        product.num -= num
        product.profit += exchange
        customer.balance -= exchange
        return True, ''
