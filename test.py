import unittest

from bakery import *


class MyTestCase(unittest.TestCase):
    def test_order(self):
        order = Order({'VS5': 10,
                       'MB11': 14,
                       'CF': 13})
        self.assertTrue('VS5' in order.products)
        self.assertTrue('MB11' in order.products)
        self.assertTrue('CF' in order.products)
        self.assertEqual(order.total_price, None)

        product_info = order.get_product('VS5')
        self.assertTrue('quantity' in product_info)
        self.assertTrue('packs' in product_info)
        self.assertTrue('total_price' in product_info)

    def test_product(self):
        product = Product('Blueberry Muffin',
                          'MB11',
                          {'5': 16.95,
                           8: '24.9599',
                           2: 9.9511111, })
        # test member format
        self.assertTrue(isinstance(product.name, str))
        self.assertTrue(isinstance(product.code, str))
        self.assertTrue(all([isinstance(quantity, int) for quantity in product.pack_sizes]))
        self.assertTrue(all([isinstance(price, Decimal) for price in product._packs.values()]))

        # test price getter and decimal places
        self.assertEqual(product.get_pack_price(5), Decimal('16.95'))
        self.assertEqual(product.get_pack_price(2), Decimal('9.95'))
        self.assertEqual(product.get_pack_price(8), Decimal('24.95'))
        self.assertEqual(abs(product.get_pack_price(2).as_tuple().exponent), DECIMAL_PLACES)

        # calculate order price
        self.assertEqual(product.get_total_price({5: 2}),
                         Decimal('16.95') * 2)
        self.assertEqual(product.get_total_price({5: 1, 2: 1, 8: 1}),
                         Decimal('16.95') + Decimal('9.95') + Decimal('24.95'))

        # test order process
        packs, rest = product.pack_order(14)
        self.assertEqual(rest, 0)
        self.assertEqual(packs, {8: 1, 2: 3})

        packs, rest = product.pack_order(15)
        self.assertEqual(rest, 0)
        self.assertEqual(packs, {8: 1, 2: 3, 5: 1})

        packs, rest = product.pack_order(1)
        self.assertEqual(rest, 1)
        self.assertEqual(packs, {})

        packs, rest = product.pack_order(3)
        self.assertEqual(rest, 1)
        self.assertEqual(packs, {2: 1})

    def test_bakery(self):
        vs = Product('Vegemite Scroll', 'VS5', {3: 6.99,
                                                5: 8.99})
        mb = Product('Blueberry Muffin', 'MB11', {2: 9.95,
                                                  5: 16.95,
                                                  8: 24.95})
        cf = Product('Croissant', 'CF', {3: 5.95,
                                         5: 9.95,
                                         9: 16.99})
        bakery = Bakery([vs, mb, cf])

        # test get product by code
        test_code = 'VS5'
        self.assertEqual(bakery.get_product('VS5').code, test_code)

        # input format test
        order_packs = bakery.process_order({'VS5': '10',
                                            'WRONG_CODE': 14,
                                            'CF': 13})
        self.assertTrue('WRONG_CODE' not in order_packs)
        self.assertTrue('VS5' in order_packs)
        self.assertTrue('CF' in order_packs)
        self.assertTrue('CF' in order_packs)

        # test single product order
        order = Order({'VS5': 10})
        bakery.process_order(order)
        self.assertEqual(order.get_product('VS5')['packs'], {'VS5': {5: 2}})

        # test combined products order
        order = Order({'VS5': 10,
                       'MB11': 14,
                       'CF': 13})
        bakery.process_order(order)
        self.assertEqual(order.get_product('VS5')['packs'], {'VS5': {5: 2}})
        self.assertEqual(order.get_product('MB11')['packs'], {'MB11': {8: 1, 2: 3}})
        self.assertEqual(order.get_product('CF')['packs'], {'CF': {5: 2, 3: 1}})
