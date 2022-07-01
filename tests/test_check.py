from datetime import date

from money.check import Check
from money.product import Product


class TestCheck:
    def test_date_1(self):
        p = Product('Product name', 1.0, 2.0)
        c = Check([p], date(2019, 1, 22))
        assert c.date_ == '22.01.2019'

    def test_date_2(self):
        p = Product('Product name', 1.0, 2.0)
        c = Check([p], date(2021, 9, 28))
        assert c.date_ == '28.09.2021'

    def test_from_json_type_1(self, datadir):
        json_file_name = str(datadir / 'check_type_1.json')

        check = Check.from_json(json_file_name)

        assert check == Check(
            [
                Product("Перевозка пассажиров и багажа", 1.0, 96.00, "ООО \"ЯНДЕКС.ТАКСИ\", taxi.yandex.ru")
            ],
            date(2022, 6, 9)
        )

    def test_from_json_type_2(self, datadir):
        json_file_name = str(datadir / "check_type_2.json")

        check = Check.from_json(json_file_name)

        assert check == Check(
            [
                Product("PAMPERS Premium Care Трусики-Подгуз 4 9-15кг ", 1.0, 1699.00,
                        "АКЦИОНЕРНОЕ ОБЩЕСТВО \"ТАНДЕР\", Магазин  Магнит  Шум"),
                Product(r"MATTEL BARBIE Бальзам для губ 2,5 гр:8/288", 1.0, 225.99,
                        "АКЦИОНЕРНОЕ ОБЩЕСТВО \"ТАНДЕР\", Магазин  Магнит  Шум"),
                Product(r"Набор бусин в асс-те (СИ):6/72", 1.0, 429.99,
                        "АКЦИОНЕРНОЕ ОБЩЕСТВО \"ТАНДЕР\", Магазин  Магнит  Шум"),
                Product("Пакет подарочный бумажный AB (МакПейпер)", 1.0, 69.90,
                        "АКЦИОНЕРНОЕ ОБЩЕСТВО \"ТАНДЕР\", Магазин  Магнит  Шум"),
            ],
            date(2022, 6, 23)
        )
