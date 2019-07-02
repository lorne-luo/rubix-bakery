import logging
from decimal import Decimal, ROUND_DOWN

# decimal is better type than float for currency due to fixed point
DECIMAL_PLACES = 2  # 10 ** -2 = 0.01
DECIMAL_UNIT = Decimal(str(10 ** (-1 * DECIMAL_PLACES)))

log = logging.getLogger(__name__)


class Bakery:
    _products = {}

    def __init__(self, products):
        for product in products:
            # skip if type not match
            if isinstance(product, Product):
                self._products[product.code] = product

    # expose as property to make sure immutable from outside
    @property
    def products(self):
        return self._products

    def process_order(self, order_dict):
        raise NotImplementedError

    def get_product(self, code):
        if code not in self._products:
            raise KeyError(f'{code} is not a code of products')
        return self._products[code]


class Product:
    _packs = {}

    def __init__(self, name, code, pack_price_dict):
        self._name = str(name)
        self._code = str(code)

        # init pack quantity and price
        for quantity, price in pack_price_dict.items():
            try:
                # simply ignore more digits, 1.999 -> 1.99
                self._packs[int(quantity)] = Decimal(str(price)).quantize(DECIMAL_UNIT, rounding=ROUND_DOWN)
            except:
                # skip invalid input, quantity must be int, price must be decimal
                pass

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

    def get_pack_price(self, quantity):
        if quantity not in self._packs:
            raise KeyError(f'{quantity} is not in {self.code}\'s pack options')
        return self._packs[quantity]

    def pack_order(self, quantity):
        raise NotImplementedError
