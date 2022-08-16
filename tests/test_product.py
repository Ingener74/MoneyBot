from datetime import date
from unittest.mock import MagicMock, call, ANY

import pytest

from money.product import Product, Products, ProductConfig


class TestProduct:
    def test_quantity_and_price_1(self):
        p = Product("Product name", 1.0, 2.0, date_of_purchase=date(2019, 1, 22))
        assert p.quantity_ == "1,0"
        assert p.price_ == "2,0"
        assert p.date_of_purchase_ == "22.01.2019"

    def test_quantity_and_price_2(self):
        p = Product("Product name", 32.0, 64.0, date_of_purchase=date(2021, 9, 28))
        assert p.quantity_ == "32,0"
        assert p.price_ == "64,0"
        assert p.date_of_purchase_ == "28.09.2021"


class TestProducts:
    def test_from_json_type_1(self, datadir):
        json_file_name = str(datadir / "check_type_1.json")

        check = Products.from_json(json_file_name)

        assert check == Products(
            [
                Product(
                    "Перевозка пассажиров и багажа",
                    1.0,
                    96.00,
                    'ООО "ЯНДЕКС.ТАКСИ", taxi.yandex.ru',
                    date_of_purchase=date(2022, 6, 9),
                )
            ]
        )

    def test_from_json_type_2(self, datadir):
        check = Products.from_json(datadir / "check_type_2.json")

        assert check == Products(
            [
                Product(
                    "PAMPERS Premium Care Трусики-Подгуз 4 9-15кг ",
                    1.0,
                    1699.00,
                    'АКЦИОНЕРНОЕ ОБЩЕСТВО "ТАНДЕР", Магазин  Магнит  Шум',
                    date_of_purchase=date(2022, 6, 23),
                ),
                Product(
                    r"MATTEL BARBIE Бальзам для губ 2,5 гр:8/288",
                    1.0,
                    225.99,
                    'АКЦИОНЕРНОЕ ОБЩЕСТВО "ТАНДЕР", Магазин  Магнит  Шум',
                    date_of_purchase=date(2022, 6, 23),
                ),
                Product(
                    r"Набор бусин в асс-те (СИ):6/72",
                    1.0,
                    429.99,
                    'АКЦИОНЕРНОЕ ОБЩЕСТВО "ТАНДЕР", Магазин  Магнит  Шум',
                    date_of_purchase=date(2022, 6, 23),
                ),
                Product(
                    "Пакет подарочный бумажный AB (МакПейпер)",
                    1.0,
                    69.90,
                    'АКЦИОНЕРНОЕ ОБЩЕСТВО "ТАНДЕР", Магазин  Магнит  Шум',
                    date_of_purchase=date(2022, 6, 23),
                ),
            ]
        )

    def test_communal_payments(self, datadir):
        check = Products.from_communal_payments(datadir / "test_com.txt")

        assert check == Products(
            [
                Product(
                    "МУП ПОВВ:ХВС ПОВЫШАЮЩИЙ КОЭФФИЦИЕНТ", 1.0, 120.82, 'МУП "ПОВВ"', date_of_purchase=date(2022, 6, 15)
                ),
                Product(
                    "ТСН ГРИНПАРК 68: ЖИЛИЩНО-КОММУНАЛЬНЫЕ УСЛУГИ",
                    1.0,
                    2015.48,
                    'ТСН "ГРИНПАРК 68"',
                    date_of_purchase=date(2022, 6, 15),
                ),
                Product(
                    'ЕРЦ УРАЛЭНЕРГОСБЫТ(ООО"НКР")ДЛЯ ООО УЭС,АО УСТЭК-ЧЕЛЯБ-СК: КОМ.',
                    1.0,
                    624.38,
                    'ОПЕРАТОР ООО "НКР" (ДЛЯ ООО "УРАЛЭНЕРГОСБЫТ" - Э/Э, ДЛЯ АО',
                    date_of_purchase=date(2022, 6, 15),
                ),
                Product("МУП ПОВВ:ВО", 1.0, 174.45, 'МУП "ПОВВ"', date_of_purchase=date(2022, 6, 15)),
                Product("МУП ПОВВ:ХВС", 1.0, 241.63, 'МУП "ПОВВ"', date_of_purchase=date(2022, 6, 15)),
                Product(
                    "УРАЛЖИЛСЕРВИС:ЗА ДОМОФОН", 1.0, 35.35, 'ООО "УРАЛЖИЛСЕРВИС"', date_of_purchase=date(2022, 6, 15)
                ),
                Product(
                    "ООО ЦКС: УСЛУГИ ОБРАЩЕНИЯ С ТКО ЧЕЛЯБИНСКИЙ КЛАСТЕР",
                    1.0,
                    86.08,
                    'ООО "ЦКС"',
                    date_of_purchase=date(2022, 6, 15),
                ),
                Product(
                    "ТСН ГРИНПАРК 68: КАПИТАЛЬНЫЙ РЕМОНТ",
                    1.0,
                    661.02,
                    'ТСН "ГРИНПАРК 68"',
                    date_of_purchase=date(2022, 6, 15),
                ),
            ],
        )

    @pytest.fixture()
    def fakes(self, mocker):
        fake_worksheet = MagicMock()
        fake_worksheet.col_values = MagicMock(return_value=["", "", "", "", "foo"])
        fake_worksheet.update = MagicMock()
        fake_worksheet.format = MagicMock()

        fake_spreadsheet = MagicMock()
        fake_spreadsheet.worksheet = MagicMock(return_value=fake_worksheet)

        fake_client = MagicMock()
        fake_client.open_by_key = MagicMock(return_value=fake_spreadsheet)
        gspread_service_account: MagicMock = mocker.patch("gspread.service_account", return_value=fake_client)

        manager = MagicMock()
        manager.attach_mock(fake_client, "client")
        manager.attach_mock(fake_spreadsheet, "spreadsheet")
        manager.attach_mock(fake_worksheet, "worksheet")
        manager.attach_mock(gspread_service_account, "service_account")
        return manager

    def test_save(self, fakes):
        products = Products([Product("Soap", 1.0, 1.0, "Seller", date_of_purchase=date(2022, 1, 1))])
        products.save_to_google_sheet(
            "creds.json", "very-long-spreadsheet-id", ProductConfig("A", "B", "C", "D", "E", "F", 0)
        )

        assert fakes.mock_calls == [
            call.service_account(filename="creds.json"),
            call.client.open_by_key("very-long-spreadsheet-id"),
            call.spreadsheet.worksheet("01.2022"),
            call.worksheet.col_values(0),
            call.worksheet.update("A6:A7", [["Soap"]], value_input_option="USER_ENTERED"),
            call.worksheet.format("A6:A6", ANY),
            call.worksheet.update("B6:B7", [["1,0"]], value_input_option="USER_ENTERED"),
            call.worksheet.format("B6:B6", ANY),
            call.worksheet.update("C6:C7", [["1,0"]], value_input_option="USER_ENTERED"),
            call.worksheet.format("C6:C6", ANY),
            call.worksheet.update("D6:D7", [["Seller"]], value_input_option="USER_ENTERED"),
            call.worksheet.format("D6:D6", ANY),
            call.worksheet.update("F6:F7", [["01.01.2022"]], value_input_option="USER_ENTERED"),
            call.worksheet.format("F6:F6", ANY),
        ]

    def test_save_with_categories(self, fakes):
        products = Products(
            [
                Product("Prod 1", 1.0, 1.0, "Seller", date_of_purchase=date(2022, 1, 2)),
                Product("Prod 2", 1.0, 2.0, "Seller", date_of_purchase=date(2022, 1, 2), category="Bread"),
                Product("Prod 3", 1.0, 3.0, "Seller", date_of_purchase=date(2022, 1, 2)),
                Product("Prod 4", 1.0, 4.0, "Seller", date_of_purchase=date(2022, 1, 2), category="Water"),
            ]
        )
        products.save_to_google_sheet(
            "creds.json", "very-long-spreadsheet-id", ProductConfig("A", "B", "C", "D", "E", "F", 0)
        )

        assert fakes.mock_calls == [
            call.service_account(filename="creds.json"),
            call.client.open_by_key("very-long-spreadsheet-id"),
            call.spreadsheet.worksheet("01.2022"),
            call.worksheet.col_values(0),
            call.worksheet.update(
                "A6:A10", [["Prod 1"], ["Prod 2"], ["Prod 3"], ["Prod 4"]], value_input_option="USER_ENTERED"
            ),
            call.worksheet.format("A6:A9", ANY),
            call.worksheet.update("B6:B10", [["1,0"], ["1,0"], ["1,0"], ["1,0"]], value_input_option="USER_ENTERED"),
            call.worksheet.format("B6:B9", ANY),
            call.worksheet.update("C6:C10", [["1,0"], ["2,0"], ["3,0"], ["4,0"]], value_input_option="USER_ENTERED"),
            call.worksheet.format("C6:C9", ANY),
            call.worksheet.update(
                "D6:D10", [["Seller"], ["Seller"], ["Seller"], ["Seller"]], value_input_option="USER_ENTERED"
            ),
            call.worksheet.format("D6:D9", ANY),
            call.worksheet.update(
                "F6:F10",
                [["02.01.2022"], ["02.01.2022"], ["02.01.2022"], ["02.01.2022"]],
                value_input_option="USER_ENTERED",
            ),
            call.worksheet.format("F6:F9", ANY),
            call.worksheet.update("E7:E8", [["Bread"]], value_input_option="USER_ENTERED"),
            call.worksheet.format("E7:E7", ANY),
            call.worksheet.update("E9:E10", [["Water"]], value_input_option="USER_ENTERED"),
            call.worksheet.format("E9:E9", ANY),
        ]

    def test_save_empty(self):
        with pytest.raises(ValueError) as ei:
            products = Products()
            products.save_to_google_sheet(
                "creds.json", "very-long-spreadsheet-id", ProductConfig("A", "B", "C", "D", "E", "F", 0)
            )
        assert str(ei.value) == "Empty products list"

    def test_different_dates(self, fakes):
        with pytest.raises(ValueError) as ei:
            products = Products(
                [
                    Product("Foo", 1.0, 1.0, date_of_purchase=date(2022, 1, 1)),
                    Product("Bar", 1.0, 1.0, date_of_purchase=date(2022, 1, 2)),
                ]
            )
            products.save_to_google_sheet(
                "creds.json", "very-long-spreadsheet-id", ProductConfig("A", "B", "C", "D", "E", "F", 0)
            )
        assert str(ei.value) == "Different dates in products"

    def test_product_names(self):
        products = Products(
            [
                Product("Prod 1", 1.0, 1.0, "Seller", date_of_purchase=date(2022, 1, 2)),
                Product("Prod 2", 1.0, 2.0, "Seller", date_of_purchase=date(2022, 1, 2), category="Bread"),
                Product("Prod 3", 1.0, 3.0, "Seller", date_of_purchase=date(2022, 1, 2)),
                Product("Prod 4", 1.0, 4.0, "Seller", date_of_purchase=date(2022, 1, 2), category="Water"),
            ]
        )

        assert (
            products.numbered_list_of_names
            == """1. Prod 1
2. Prod 2
3. Prod 3
4. Prod 4"""
        )
