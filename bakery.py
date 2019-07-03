import logging
import sys
from decimal import Decimal, ROUND_DOWN

# decimal is better type than float for currency due to fixed point
DECIMAL_PLACES = 2  # 10 ** -2 = 0.01
DECIMAL_UNIT = Decimal(str(10 ** (-1 * DECIMAL_PLACES)))

logger = logging.getLogger(__name__)


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
    total_price = None

    def __init__(self, order_dict):
        """
        :param order_dict: dict of product code and quantity
        """
        for code, quantity in order_dict.items():
            self._products[code] = {
                'quantity': quantity,
                'packs': {},
                'total_price': None
            }

    # expose as property to make sure immutable from outside
    @property
    def products(self):
        return self._products

    def get_product(self, code):
        if code not in self._products:
            raise KeyError(f'{code} is not in this order.')
        return self._products[code]


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
        """quantity list of available packs with descending sort"""
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
            if rest == 0:
                break
        return result, rest

    def pack_order(self, quantity):
        """return pack match as dict and remainder"""
        try:
            quantity = int(quantity)
        except:
            raise Exception('invalid quantity, should be int')

        pack_set = {}

        # self.pack_quantity is in descending sort, so prior to put large size pack in
        return self._fill(pack_set, quantity, self.pack_quantity)

    def _fill(self, pack_dict, remainder_quantity, pack_sizes):
        """
        recursive function to breakdown quantity into pack set
        :param pack_dict: dict of pack size and pack amount to indicate what and how many pack already in
        :param remainder_quantity: remainder of how many still need to be break down
        :param pack_sizes: available pack size in this recursion
        :return: dict of pack breakdown and remainder
        """
        logger.debug('Call _fill()', pack_dict, remainder_quantity, pack_sizes)

        for i in range(len(pack_sizes)):
            pack_quantity = pack_sizes[i]
            pack_amount, remainder_quantity = int(
                remainder_quantity / pack_quantity), remainder_quantity % pack_quantity

            if pack_amount > 0:
                # some pack could be added into the pack set
                pack_dict[pack_quantity] = pack_amount

            if remainder_quantity == 0 or not pack_sizes[i + 1:]:
                # return directly if remainder is 0 or no smaller pack size available
                logger.debug('_fill() return', pack_dict, remainder_quantity)
                return pack_dict, remainder_quantity

            for j in range(pack_amount):
                pack_dict, remainder_quantity = self._fill(pack_dict, remainder_quantity, pack_sizes[i + 1:])
                if remainder_quantity > 0:
                    pack_dict, remainder_quantity = self._pop_smallest_pack(pack_dict, remainder_quantity)

                if remainder_quantity == 0 or not pack_sizes[i + 1:]:
                    # return directly if remainder is 0 or no smaller pack size available
                    logger.debug('_fill() return', pack_dict, remainder_quantity)
                    return pack_dict, remainder_quantity

        return pack_dict, remainder_quantity

    def _pop_smallest_pack(self, pack_dict, remainder):
        """
        pop one smallest pack back to remainder
        :param pack_dict: dict of pack size and pack amount
        :param remainder: remainder
        :return: pack_dict, remainder
        """
        pack_size = list(pack_dict.keys())
        pack_size.sort()

        for size in pack_size:
            if size in pack_dict and pack_dict[size] > 0:
                if pack_dict[size] == 1:
                    pack_dict.pop(size)
                else:
                    pack_dict[size] -= 1
                remainder += size
                return pack_dict, remainder
        return pack_dict, remainder
