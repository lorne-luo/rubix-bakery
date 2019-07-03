from models.bakery import Bakery
from models.order import Order
from models.product import Product


def print_product(product):
    print('%-20s %s' % ('Name:', product.name))
    print('%-20s %s' % ('Code:', product.code))
    for index, size in enumerate(product.packs):
        title = 'Pack Size:' if index == 0 else ''
        print('%-20s %s' % (title, f'{size}: ${product.packs[size]}'))
    print('-' * 40)


def print_order(order, bakery):
    for code, product in order.products.items():
        name = bakery.get_product(code).name
        print('%-20s %s' % (f'{name}:', product['quantity']))


def print_result(order, bakery):
    for code, order_product in order.products.items():
        product = bakery.get_product(code)
        print('%-20s %s' % (f'{product.name}:', product.pack_sizes))
        print('%-20s %s' % (f'Pack breakdown:', order_product['quantity']))
        if not order_product['packs']:
            print('%-10s %s' % ('', f'Non pack matches'))
        else:
            for index, size in enumerate(order_product['packs']):
                pack_price = product.get_pack_price(size)
                amount = order_product["packs"][size]
                print('%-2s %-17s %-12s %s' % ('',
                                               f'Pack of {size} X {amount}',
                                               f'{size*amount}',
                                               f'${pack_price} X {amount}'))
        print('%-20s %s' % (f'Remainder:', order_product['remainder']))
        print('%-20s %-12s $%s' % (f'Total Price:', '', order_product['total_price']))
        print('-' * 50)


if __name__ == '__main__':
    vs = Product('Vegemite Scroll', 'VS5', {3: 6.99,
                                            5: 8.99})
    mb = Product('Blueberry Muffin', 'MB11', {2: 9.95,
                                              5: 16.95,
                                              8: 24.95})
    cf = Product('Croissant', 'CF', {3: 5.95,
                                     5: 9.95,
                                     9: 16.99})
    bakery = Bakery([vs, mb, cf])

    print('Welcome to Rubix bakery, we provide:')
    print('=' * 60)

    for code, product in bakery.products.items():
        print_product(product)

    product_quantity = {}
    for code, product in bakery.products.items():
        print(f'Please input how many {product.name} you want:')

        while (not product_quantity.get(code, '').isdigit()):
            product_quantity[code] = input()
            if not product_quantity[code].isdigit():
                print(f'`{product_quantity[code]}` is invalid input, please input a number for {product.name}:')

    order = Order(product_quantity)

    bakery.process_order(order)
    print(f'\n\nYour best pack breakdown:')
    print('=' * 60)
    print_result(order, bakery)
