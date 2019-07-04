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

    def process_order(self, order):
        """
        :param order: order object
        :return: order object
        """
        for product_code, order_product in order.products.items():
            quantity = order_product.get("quantity")
            if product_code not in self._products:
                # skip invalid product code
                continue

            # call product.pack_order to break down quantity
            packs, remainder, total_price = self.get_product(product_code).pack_order(
                quantity
            )
            order.set_product_break_down(product_code, packs, remainder, total_price)

    def get_product(self, code):
        """
        get product by code
        """
        if code not in self._products:
            raise KeyError(f"{code} is not a code of products")
        return self._products[code]
