import logging
from decimal import Decimal, ROUND_DOWN

from config import PRICE_DECIMAL_UNIT
from helper import pack_breakdown

logger = logging.getLogger(__name__)


class Product:

    def __init__(self, name, code, pack_price_dict):
        """
        :param name: name of product
        :param code: code of product
        :param pack_price_dict: dict of pack size and price
        """
        self._name = str(name)
        self._code = str(code)
        self._packs = {}

        # init pack quantity and price
        for quantity, price in pack_price_dict.items():
            try:
                # simply ignore more digits, 1.999 -> 1.99
                self._packs[int(quantity)] = Decimal(str(price)).quantize(PRICE_DECIMAL_UNIT, rounding=ROUND_DOWN)
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
    def pack_sizes(self):
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
        total_price = 0
        for pack_size, pack_amount in order_dict.items():
            # invalid pack size, skip
            if pack_size in self._packs:
                total_price += self.get_pack_price(pack_size) * pack_amount

        return total_price

    def _quick_pack(self, quantity):
        """
        most greedy way to match the order, so if perfect match exist it will get quick response
        :param quantity:
        :return: dict of pack size, pack amount and total price
        """
        result = {}
        rest = quantity
        for i in self.pack_sizes:
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

        # self.pack_sizes is in descending sort, so prior to put large size pack in
        pack_dict, remainder = pack_breakdown(quantity, self.pack_sizes)

        # remove pack size if amount == 0, pack_dict can be empty dict
        if pack_dict:
            pack_dict = dict([x for x in pack_dict.items() if x[1]])

        return pack_dict, remainder, self.get_total_price(pack_dict)
