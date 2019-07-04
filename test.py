import os
import random
import unittest
from decimal import Decimal

from config import PRICE_DECIMAL_PLACES, env_bool, env_int
from helper import rank_breakdown, pack_breakdown
from models.bakery import Bakery
from models.order import Order
from models.product import Product


def generate_random_list(dimension=None, value_upper_bound=20):
    """
    :param dimension: if not provide will generate a random length list 
    :param value_upper_bound: 
    :return: 
    """
    random_list = []

    dimension = dimension or random.randrange(1, 5)  # how many pack have, up to 5

    # this is important to prevent loop forever
    value_upper_bound = (
        value_upper_bound if value_upper_bound > dimension else dimension
    )

    for i in range(dimension):
        while True:
            value_candidate = random.randrange(
                dimension, value_upper_bound
            )  # random pack size, upper bound 20
            if value_candidate in random_list:
                # continue if already in, pack size should be unique
                continue
            random_list.append(value_candidate)
            break

    return random_list


class BakeryTestCase(unittest.TestCase):
    def test_rank_breakdown(self):
        # brutal random test
        for quantity in range(200):
            # random generate pack size with random dimension
            random_pack_sizes = generate_random_list()
            random_pack_sizes.sort(reverse=True)  # pack sizes should be descending

            # run rank_breakdown with all random input
            breakdown_candidates = rank_breakdown(quantity, random_pack_sizes)

            # loop all solution candidates
            for breakdown in breakdown_candidates:
                total = sum(
                    [
                        random_pack_sizes[i] * breakdown[i]
                        for i in range(len(random_pack_sizes))
                    ]
                )

                # criteria 1: total quantity should not excess quantity (all too-much solution excluded)
                self.assertTrue(total <= quantity)

                # criteria 2: quantity - total < max(random_pack_sizes) (all too-less solution excluded)
                self.assertTrue(quantity - total < max(random_pack_sizes))

    def test_pack_breakdown(self):
        # reverse random test
        # give any quantity which known have prefect match, the remainder should always 0
        for i in range(100):  # random test 100 times
            random_pack_sizes = generate_random_list()
            random_pack_sizes.sort(reverse=True)  # pack sizes should be descending
            random_packs_amount = generate_random_list(
                dimension=len(random_pack_sizes)
            )  # generate a random breakdown

            perfect_quantity = sum(
                [
                    random_pack_sizes[i] * random_packs_amount[i]
                    for i in range(len(random_pack_sizes))
                ]
            )

            packs_amount, remainder = pack_breakdown(
                perfect_quantity, random_pack_sizes
            )
            # print(i, random_pack_sizes, random_packs_amount, perfect_quantity)
            # accept criteria, remainder should always 0
            self.assertEqual(remainder, 0)

    def test_config(self):
        # test env_bool
        self.assertRaises(Exception, env_bool, "NOT_EXIST")
        self.assertEqual(env_bool("NOT_EXIST", 2), True)
        self.assertEqual(env_bool("NOT_EXIST", 0), False)
        self.assertEqual(env_bool("NOT_EXIST", "3"), True)
        self.assertEqual(env_bool("NOT_EXIST", "false"), False)
        os.environ["DEBUG"] = "1"
        self.assertEqual(env_bool("DEBUG"), True)

        # test env_int
        self.assertRaises(Exception, env_int, "NOT_EXIST")
        self.assertRaises(Exception, env_int, "NOT_EXIST", "NOT_NUMBER")
        self.assertEqual(env_int("NOT_EXIST", 2), 2)
        self.assertEqual(env_int("NOT_EXIST", "3"), 3)
        os.environ["PRICE_DECIMAL_PLACES"] = "1"
        self.assertEqual(env_int("PRICE_DECIMAL_PLACES"), 1)
        self.assertEqual(env_int("PRICE_DECIMAL_PLACES", 2), 1)

    def test_order(self):
        order = Order({"VS5": 10, "MB11": 14, "CF": 13})
        self.assertTrue("VS5" in order.products)
        self.assertTrue("MB11" in order.products)
        self.assertTrue("CF" in order.products)
        self.assertEqual(order.total_price, None)

        product_info = order.get_product("VS5")
        self.assertTrue("quantity" in product_info)
        self.assertTrue("packs" in product_info)
        self.assertTrue("total_price" in product_info)

        self.assertRaises(KeyError, order.get_product, "not_exist_code")

    def test_product(self):
        product = Product(
            "Blueberry Muffin", "MB11", {"5": 16.95, 8: "24.9599", 2: 9.9511111}
        )
        # test member format
        self.assertTrue(isinstance(product.name, str))
        self.assertTrue(isinstance(product.code, str))
        self.assertTrue(
            all([isinstance(quantity, int) for quantity in product.pack_sizes])
        )
        self.assertTrue(
            all([isinstance(price, Decimal) for price in product._packs.values()])
        )

        # test price getter and decimal places
        self.assertEqual(product.get_pack_price(5), Decimal("16.95"))
        self.assertEqual(product.get_pack_price(2), Decimal("9.95"))
        self.assertEqual(product.get_pack_price(8), Decimal("24.95"))
        self.assertRaises(KeyError, product.get_pack_price, 100)
        self.assertEqual(
            abs(product.get_pack_price(2).as_tuple().exponent), PRICE_DECIMAL_PLACES
        )

        # calculate order price
        self.assertEqual(product.get_total_price({5: 2}), Decimal("16.95") * 2)
        self.assertEqual(
            product.get_total_price({5: 1, 2: 1, 8: 1}),
            Decimal("16.95") + Decimal("9.95") + Decimal("24.95"),
        )

        # ignore invalid pack size
        self.assertEqual(
            product.get_total_price({5: 1, 2: 1, 100: 1}),
            Decimal("16.95") + Decimal("9.95"),
        )

        # test order process
        self.assertRaises(
            Exception, product.pack_order, "INVALID_INPUT"
        )  # test invalid input

        packs, rest, total_price = product.pack_order(14)
        self.assertEqual(rest, 0)
        self.assertEqual(packs, {8: 1, 2: 3})
        self.assertEqual(total_price, Decimal("24.95") * 1 + Decimal("9.95") * 3)

        packs, rest, total_price = product.pack_order(15)
        self.assertEqual(rest, 0)
        self.assertEqual(packs, {8: 1, 2: 1, 5: 1})
        self.assertEqual(
            total_price,
            Decimal("24.95") * 1 + Decimal("9.95") * 1 + Decimal("16.95") * 1,
        )

        packs, rest, total_price = product.pack_order(1)
        self.assertEqual(rest, 1)
        self.assertEqual(packs, {})
        self.assertEqual(total_price, 0)

        packs, rest, total_price = product.pack_order(3)
        self.assertEqual(packs, {2: 1})
        self.assertEqual(rest, 1)
        self.assertEqual(total_price, Decimal("9.95") * 1)

    def test_bakery(self):
        vs = Product("Vegemite Scroll", "VS5", {3: 6.99, 5: 8.99})
        mb = Product("Blueberry Muffin", "MB11", {2: 9.95, 5: 16.95, 8: 24.95})
        cf = Product("Croissant", "CF", {3: 5.95, 5: 9.95, 9: 16.99})
        bakery = Bakery([vs, mb, cf])

        # test get product by code
        test_code = "VS5"
        self.assertEqual(bakery.get_product("VS5").code, test_code)
        self.assertRaises(KeyError, bakery.get_product, "not_exist_code")

        # init order for test
        order = Order({"VS5": "10", "WRONG_CODE": 14, "CF": 13})
        # input format test
        bakery.process_order(order)
        self.assertTrue(order.get_product("WRONG_CODE")["total_price"] is None)

        # test single product order
        order = Order({"VS5": 10})
        bakery.process_order(order)
        self.assertEqual(order.get_product("VS5")["packs"], {5: 2})

        # test combined products order
        order = Order({"VS5": 10, "MB11": 14, "CF": 13})
        bakery.process_order(order)
        self.assertEqual(order.get_product("VS5")["packs"], {5: 2})
        self.assertEqual(order.get_product("VS5")["remainder"], 0)
        self.assertEqual(order.get_product("MB11")["packs"], {8: 1, 2: 3})
        self.assertEqual(order.get_product("MB11")["remainder"], 0)
        self.assertEqual(order.get_product("CF")["remainder"], 0)
        self.assertEqual(order.get_product("CF")["packs"], {5: 2, 3: 1})
