import logging

logger = logging.getLogger(__name__)


class Order:
    def __init__(self, order_dict):
        """
        :param order_dict: dict of product code and quantity
        """
        self._products = {}
        self.total_price = None

        for code, quantity in order_dict.items():
            # init a dict of product, using code as dict key
            self._products[code] = {
                "quantity": quantity,
                "packs": {},  # to contain pack breakdown result
                "remainder": None,  # remainder if this product cant be perfectly break down
                "total_price": None,
            }

    # expose as property to make sure immutable from outside
    @property
    def products(self):
        return self._products

    def get_product(self, code):
        if code not in self._products:
            raise KeyError(f"{code} is not in this order.")
        return self._products[code]

    def set_product_break_down(self, product_code, packs, remainder, total_price):
        if product_code not in self._products:
            raise KeyError(f"{product_code} is not in this order.")
        self._products[product_code]["packs"] = packs
        self._products[product_code]["remainder"] = remainder
        self._products[product_code]["total_price"] = total_price
