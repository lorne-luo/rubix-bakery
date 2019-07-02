import logging
from decimal import Decimal, ROUND_DOWN

# decimal is better type than float for currency due to fixed point
DECIMAL_PLACES = 2  # 10 ** -2 = 0.01
DECIMAL_UNIT = Decimal(str(10 ** (-1 * DECIMAL_PLACES)))

log = logging.getLogger(__name__)


class Bakery:
    _products = {}

    def __init__(self, products):
        """
        :param products: list of product object
        """
        for product in products:
            # skip if type not match
            if isinstance(product, Product):
                self._products[product.code] = product

    # expose as property to make sure immutable from outside
    @property
    def products(self):
        return self._products

    def process_order(self, order_dict):
        """
        :param order_dict: dict of product code and amount
        :return: pack result of entire order
        """
        raise NotImplementedError

    def get_product(self, code):
        """
        get product by code
        """
        if code not in self._products:
            raise KeyError(f'{code} is not a code of products')
        return self._products[code]


class Order:
    _products = {}

    def __init__(self, order_dict):
        """
        :param order_dict: dict of product code and amount
        """
        raise NotImplementedError

    # expose as property to make sure immutable from outside
    @property
    def products(self):
        return self.products

    def get_product(self, code):
        raise NotImplementedError


class Product:
    _packs = {}

    def __init__(self, name, code, pack_price_dict):
        """
        :param name: name of product
        :param code: code of product
        :param pack_price_dict: dict of pack size and price
        """
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
        """quantity list of available packs"""
        quantity_options = list(self._packs.keys())
        quantity_options.sort(reverse=True)
        return quantity_options

    def get_pack_price(self, quantity):
        """
        :param quantity: pack quantity
        :return: price for specified quantity pack, raise error if not exist
        """
        if quantity not in self._packs:
            raise KeyError(f'{quantity} is not in {self.code}\'s pack options')
        return self._packs[quantity]

    def get_total_price(self, order_dict):
        """
        :param order_dict: pack size and amount
        :return: total price
        """
        raise NotImplementedError

    def _quick_pack(self, quantity):
        """
        most greedy way to match the order, so if perfect match exist it will get quick response
        :param quantity:
        :return: dict of pack size and amount
        """
        result = {}
        rest = quantity
        for i in self.pack_quantity:
            pack_amount, rest = int(rest / i), rest % i
            result[i] = pack_amount
            print(rest)
        print(result, rest)

    def pack_order(self, quantity):
        """"""
        raise NotImplementedError
