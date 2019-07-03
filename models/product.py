import logging
from decimal import Decimal, ROUND_DOWN

from config import PRICE_DECIMAL_UNIT

logger = logging.getLogger(__name__)


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
        raise NotImplementedError

    def _quick_pack(self, quantity):
        """
        most greedy way to match the order, so if perfect match exist it will get quick response
        :param quantity:
        :return: dict of pack size and amount
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

        pack_set = {}

        # self.pack_sizes is in descending sort, so prior to put large size pack in
        return self._fill(pack_set, quantity, self.pack_sizes)

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
            pack_size = pack_sizes[i]
            pack_amount, remainder_quantity = int(
                remainder_quantity / pack_size), remainder_quantity % pack_size

            if pack_amount > 0:
                # some pack could be added into the pack set
                pack_dict[pack_size] = pack_amount

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
