import logging

from models.product import Product

logger = logging.getLogger(__name__)


class Bakery:

    def __init__(self, products):
        """
        :param products: list of product object
        """
        self._products = {}

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
