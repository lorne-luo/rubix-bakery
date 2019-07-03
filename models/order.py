import logging

logger = logging.getLogger(__name__)



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
