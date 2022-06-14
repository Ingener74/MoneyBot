from datetime import date

from money.product import Product


class TestProduct:
    def test_quantity_and_price_1(self):
        p = Product('Product name', 1.0, 2.0, 'Seller', date(2019, 1, 22))
        assert p.quantity_ == '1,0'
        assert p.price_ == '2,0'
        assert p.date_ == '22.01.2019'

    def test_quantity_and_price_2(self):
        p = Product('Product name', 32.0, 64.0, 'Seller', date(2021, 9, 28))
        assert p.quantity_ == '32,0'
        assert p.price_ == '64,0'
        assert p.date_ == '28.09.2021'
