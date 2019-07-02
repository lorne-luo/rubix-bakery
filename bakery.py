import logging
from decimal import Decimal, ROUND_DOWN


class Bakery:
    _products = {}

    def __init__(self, *products):
        raise NotImplementedError

    def process_order(self, order_dict):
        raise NotImplementedError

    # expose as property to make sure immutable from outside
    @property
    def products(self):
        return self._products


    def get_product(self, code):
        if code not in self._products:
            raise KeyError(f'{code} is not a code of products')
        return self._products[code]


class Product:
    _packs = {}

    def __init__(self, name, code, pack_price_dict):
        raise NotImplementedError


    def get_pack_price(self, quantity):
        return self._packs[quantity]

    # expose as property to make sure immutable from outside
    @property
    def packs(self):
        return self._packs

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def pack_quantity(self):
        quantity_options = list(self._packs.keys())
        quantity_options.sort()
        return quantity_options

    def pack_order(self,quantity):
        raise NotImplementedError

