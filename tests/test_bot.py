from datetime import datetime
from unittest.mock import call, MagicMock, mock_open, ANY

import pytest

from bot.processor import process_check
from bot.settings import Settings, ExtractMethod
from bot.utils import write_execution_time
from money.product import ProductConfig


def test_write_execution_time(mocker):
    m = mocker.patch("bot.utils.open")

    write_execution_time("benchmarks.txt", True, 1.0, datetime(2022, 6, 17, 10, 0, 0), "./foo.png")

    assert m.mock_calls == [
        call("benchmarks.txt", "a"),
        call().__enter__(),
        call().__enter__().write("./foo.png;True;10:00:00-17.06.2022;1.00\n"),
        call().__exit__(None, None, None),
    ]


class TestBot:
    @pytest.fixture
    def fakes(self, mocker):
        mocker.patch("os.environ", new={"PROVERKA_CHECKA_TOKEN": "prov-check-token", "MONEY_SPREEDSHEET": "money-id"})

        open_mock: MagicMock = mocker.patch("money.api_check_extractor.open")
        product_open_mock: MagicMock = mocker.patch("money.product.open")
        post_mock: MagicMock = mocker.patch("requests.post")

        shutil_copy_mock: MagicMock = mocker.patch("shutil.copy")

        reformat_json_mock: MagicMock = mocker.patch("bot.processor.reformat_json")

        save_to_google_sheet_mock: MagicMock = mocker.patch("money.product.Products.save_to_google_sheet")

        manager = MagicMock()
        manager.attach_mock(post_mock, "post")
        manager.attach_mock(shutil_copy_mock, "copy")
        manager.attach_mock(reformat_json_mock, "reformat_json")
        manager.attach_mock(save_to_google_sheet_mock, "save_to_google_sheet")
        manager.attach_mock(product_open_mock, "product_open")
        manager.attach_mock(open_mock, "check_extractor_open")
        return manager

    def test_process_photo(self, fakes, datadir):
        response = MagicMock()
        response.text = r'{"code":1,"first":0,"data":{"json":{"code":3,"user":"ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ \"АГРОТОРГ\"","items":[{"nds":2,"sum":19439,"name":"Дск Яблоко красное 1кг","price":15999,"quantity":1.215,"paymentType":4,"productType":1,"itemsQuantityMeasure":11},{"nds":2,"sum":7999,"name":"ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м\/у 1л","price":7999,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4607036340658","sernum":"","productIdType":3,"rawProductCode":"4607036340658"}},"itemsQuantityMeasure":0},{"nds":2,"sum":7999,"name":"ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м\/у 1л","price":7999,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4607036340658","sernum":"","productIdType":3,"rawProductCode":"4607036340658"}},"itemsQuantityMeasure":0},{"nds":2,"sum":5999,"name":"*ШАР.Ваф.ВЕН.со взб.сл\/виш.150г","price":5999,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4604386012273","sernum":"","productIdType":3,"rawProductCode":"4604386012273"}},"itemsQuantityMeasure":0},{"nds":1,"sum":9499,"name":"Вафли ЯШКИНСКИЕ ореховые   300г","price":9499,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4607015232646","sernum":"","productIdType":3,"rawProductCode":"4607015232646"}},"itemsQuantityMeasure":0}],"nds10":3766,"nds18":1583,"region":"74","userInn":"7825706086  ","dateTime":"2022-08-16T19:11:00","kktRegId":"0004000518016307    ","metadata":{"id":4373135767659163393,"ofdId":"ofd22","address":"454100,Россия,Челябинская область,Челябинский г.о.,Курчатовский г.п.,Челябинск г,,Новоградский пр-кт,,д. 58,,,,","subtype":"receipt","receiveDate":"2022-08-16T17:13:18Z"},"operator":"Котова Анна Романовна, Продавец-каccир","totalSum":50935,"creditSum":0,"numberKkt":"00105702181010","fiscalSign":147824925,"prepaidSum":0,"retailPlace":"385H; 18300 - Пятерочка;","shiftNumber":302,"cashTotalSum":0,"provisionSum":0,"ecashTotalSum":50935,"operationType":1,"redefine_mask":2,"requestNumber":408,"fiscalDriveNumber":"9960440301310853","messageFiscalSign":9.29735071111385e+18,"retailPlaceAddress":"454000, 74, г.Челябинск, р-н Курчатовский, пр-кт Новоградский, 58;","appliedTaxationType":1,"fiscalDocumentNumber":77916,"fiscalDocumentFormatVer":4},"html":"<table class=\"b-check_table table\"><tbody><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ \"АГРОТОРГ\"<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">454000, 74, г.Челябинск, р-н Курчатовский, пр-кт Новоградский, 58;<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">ИНН 7825706086  <\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">&nbsp;<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">16.08.2022 19:11<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">Чек № 408<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">Смена № 302<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">Кассир Котова Анна Романовна, Продавец-каccир<\/td><\/tr><tr class=\"b-check_vblock-last b-check_center\"><td colspan=\"5\">Приход<\/td><\/tr><tr><td><strong>№<\/strong><\/td><td><strong>Название<\/strong><\/td><td><strong>Цена<\/strong><\/td><td><strong>Кол.<\/strong><\/td><td><strong>Сумма<\/strong><\/td><\/tr><tr class=\"b-check_item\"><td>1<\/td><td>Дск Яблоко красное 1кг<\/td><td>159.99<\/td><td>1.215<\/td><td>194.39<\/td><\/tr><tr class=\"b-check_item\"><td>2<\/td><td>ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м\/у 1л<\/td><td>79.99<\/td><td>1<\/td><td>79.99<\/td><\/tr><tr class=\"b-check_item\"><td>3<\/td><td>ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м\/у 1л<\/td><td>79.99<\/td><td>1<\/td><td>79.99<\/td><\/tr><tr class=\"b-check_item\"><td>4<\/td><td>*ШАР.Ваф.ВЕН.со взб.сл\/виш.150г<\/td><td>59.99<\/td><td>1<\/td><td>59.99<\/td><\/tr><tr class=\"b-check_item\"><td>5<\/td><td>Вафли ЯШКИНСКИЕ ореховые   300г<\/td><td>94.99<\/td><td>1<\/td><td>94.99<\/td><\/tr><tr class=\"b-check_vblock-first\"><td colspan=\"3\" class=\"b-check_itogo\">ИТОГО:<\/td><td><\/td><td class=\"b-check_itogo\">509.35<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"3\">Наличные<\/td><td><\/td><td>0.00<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"3\">Карта<\/td><td><\/td><td>509.35<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"3\">НДС итога чека со ставкой 20%<\/td><td><\/td><td>15.83<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"3\">НДС итога чека со ставкой 10%<\/td><td><\/td><td>37.66<\/td><\/tr><tr class=\"b-check_vblock-last\"><td colspan=\"5\">ВИД НАЛОГООБЛОЖЕНИЯ: ОСН<\/td><\/tr><tr class=\"b-check_vblock-first\"><td colspan=\"5\">РЕГ.НОМЕР ККТ: 0004000518016307    <\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"5\">ЗАВОД. №: <\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"5\">ФН: 9960440301310853<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"5\">ФД: 77916<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"5\">ФПД#: 147824925<\/td><\/tr><tr class=\"b-check_vblock-last\"><td colspan=\"5\" class=\"b-check_center\"><img src=\"\/qrcode\/generate?text=t%3D20220816T1911%26s%3D509.35%26fn%3D9960440301310853%26i%3D77916%26fp%3D147824925%26n%3D1\" alt=\"QR код чека\" width=\"35%\" loading=\"lazy\" decoding=\"async\"><\/td><\/tr><\/tbody><\/table>"}}'  # noqa: E501
        response.status_code = 200
        fakes.post.return_value = response

        mock_open(
            fakes.product_open,
            read_data=r'{"code":3,"user":"ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ \"АГРОТОРГ\"","items":[{"nds":2,"sum":19439,"name":"Дск Яблоко красное 1кг","price":15999,"quantity":1.215,"paymentType":4,"productType":1,"itemsQuantityMeasure":11},{"nds":2,"sum":7999,"name":"ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м\/у 1л","price":7999,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4607036340658","sernum":"","productIdType":3,"rawProductCode":"4607036340658"}},"itemsQuantityMeasure":0},{"nds":2,"sum":7999,"name":"ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м\/у 1л","price":7999,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4607036340658","sernum":"","productIdType":3,"rawProductCode":"4607036340658"}},"itemsQuantityMeasure":0},{"nds":2,"sum":5999,"name":"*ШАР.Ваф.ВЕН.со взб.сл\/виш.150г","price":5999,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4604386012273","sernum":"","productIdType":3,"rawProductCode":"4604386012273"}},"itemsQuantityMeasure":0},{"nds":1,"sum":9499,"name":"Вафли ЯШКИНСКИЕ ореховые   300г","price":9499,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4607015232646","sernum":"","productIdType":3,"rawProductCode":"4607015232646"}},"itemsQuantityMeasure":0}],"nds10":3766,"nds18":1583,"region":"74","userInn":"7825706086  ","dateTime":"2022-08-16T19:11:00","kktRegId":"0004000518016307    ","metadata":{"id":4373135767659163393,"ofdId":"ofd22","address":"454100,Россия,Челябинская область,Челябинский г.о.,Курчатовский г.п.,Челябинск г,,Новоградский пр-кт,,д. 58,,,,","subtype":"receipt","receiveDate":"2022-08-16T17:13:18Z"},"operator":"Котова Анна Романовна, Продавец-каccир","totalSum":50935,"creditSum":0,"numberKkt":"00105702181010","fiscalSign":147824925,"prepaidSum":0,"retailPlace":"385H; 18300 - Пятерочка;","shiftNumber":302,"cashTotalSum":0,"provisionSum":0,"ecashTotalSum":50935,"operationType":1,"redefine_mask":2,"requestNumber":408,"fiscalDriveNumber":"9960440301310853","messageFiscalSign":9.29735071111385e+18,"retailPlaceAddress":"454000, 74, г.Челябинск, р-н Курчатовский, пр-кт Новоградский, 58;","appliedTaxationType":1,"fiscalDocumentNumber":77916,"fiscalDocumentFormatVer":4}',
            # noqa: E501
        )

        result = process_check(datadir / "foo.jpg")

        assert (
            result
            == """1. Дск Яблоко красное 1кг
2. ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м/у 1л
3. ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м/у 1л
4. *ШАР.Ваф.ВЕН.со взб.сл/виш.150г
5. Вафли ЯШКИНСКИЕ ореховые   300г"""
        )

        assert fakes.mock_calls == [
            call.check_extractor_open(datadir / "foo.jpg", "rb"),
            call.post(
                "https://proverkacheka.com/api/v1/check/get", data={"token": "prov-check-token"}, files={"qrfile": ANY}
            ),
            call.check_extractor_open(datadir / "foo.json", "w"),
            call.check_extractor_open().__enter__(),
            call.check_extractor_open().__enter__().write(open(datadir / "test_process_photo/foo.json").read()),
            call.check_extractor_open().__exit__(None, None, None),
            call.product_open(str(datadir / "foo.json"), "r", encoding="utf-8"),
            call.product_open().__enter__(),
            call.product_open().read(),
            call.product_open().__exit__(None, None, None),
            call.copy(datadir / "foo.json", datadir / "foo.orig.json"),
            call.reformat_json(datadir / "foo.json", datadir / "foo.reformat.json"),
            call.save_to_google_sheet(
                "creds.json",
                "money-id",
                ProductConfig(
                    name_column="I",
                    quantity_column="K",
                    price_column="L",
                    seller_column="N",
                    category_column="J",
                    date_column="O",
                    current_products_column=9,
                ),
            ),
        ]

    def test_process_photo_error(self, fakes, datadir):
        response = MagicMock()
        response.text = r'{"code":0,"first":0,"data":{"json":{"code":3,"user":"ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ \"АГРОТОРГ\"","items":[{"nds":2,"sum":19439,"name":"Дск Яблоко красное 1кг","price":15999,"quantity":1.215,"paymentType":4,"productType":1,"itemsQuantityMeasure":11},{"nds":2,"sum":7999,"name":"ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м\/у 1л","price":7999,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4607036340658","sernum":"","productIdType":3,"rawProductCode":"4607036340658"}},"itemsQuantityMeasure":0},{"nds":2,"sum":7999,"name":"ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м\/у 1л","price":7999,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4607036340658","sernum":"","productIdType":3,"rawProductCode":"4607036340658"}},"itemsQuantityMeasure":0},{"nds":2,"sum":5999,"name":"*ШАР.Ваф.ВЕН.со взб.сл\/виш.150г","price":5999,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4604386012273","sernum":"","productIdType":3,"rawProductCode":"4604386012273"}},"itemsQuantityMeasure":0},{"nds":1,"sum":9499,"name":"Вафли ЯШКИНСКИЕ ореховые   300г","price":9499,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4607015232646","sernum":"","productIdType":3,"rawProductCode":"4607015232646"}},"itemsQuantityMeasure":0}],"nds10":3766,"nds18":1583,"region":"74","userInn":"7825706086  ","dateTime":"2022-08-16T19:11:00","kktRegId":"0004000518016307    ","metadata":{"id":4373135767659163393,"ofdId":"ofd22","address":"454100,Россия,Челябинская область,Челябинский г.о.,Курчатовский г.п.,Челябинск г,,Новоградский пр-кт,,д. 58,,,,","subtype":"receipt","receiveDate":"2022-08-16T17:13:18Z"},"operator":"Котова Анна Романовна, Продавец-каccир","totalSum":50935,"creditSum":0,"numberKkt":"00105702181010","fiscalSign":147824925,"prepaidSum":0,"retailPlace":"385H; 18300 - Пятерочка;","shiftNumber":302,"cashTotalSum":0,"provisionSum":0,"ecashTotalSum":50935,"operationType":1,"redefine_mask":2,"requestNumber":408,"fiscalDriveNumber":"9960440301310853","messageFiscalSign":9.29735071111385e+18,"retailPlaceAddress":"454000, 74, г.Челябинск, р-н Курчатовский, пр-кт Новоградский, 58;","appliedTaxationType":1,"fiscalDocumentNumber":77916,"fiscalDocumentFormatVer":4},"html":"<table class=\"b-check_table table\"><tbody><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ \"АГРОТОРГ\"<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">454000, 74, г.Челябинск, р-н Курчатовский, пр-кт Новоградский, 58;<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">ИНН 7825706086  <\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">&nbsp;<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">16.08.2022 19:11<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">Чек № 408<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">Смена № 302<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">Кассир Котова Анна Романовна, Продавец-каccир<\/td><\/tr><tr class=\"b-check_vblock-last b-check_center\"><td colspan=\"5\">Приход<\/td><\/tr><tr><td><strong>№<\/strong><\/td><td><strong>Название<\/strong><\/td><td><strong>Цена<\/strong><\/td><td><strong>Кол.<\/strong><\/td><td><strong>Сумма<\/strong><\/td><\/tr><tr class=\"b-check_item\"><td>1<\/td><td>Дск Яблоко красное 1кг<\/td><td>159.99<\/td><td>1.215<\/td><td>194.39<\/td><\/tr><tr class=\"b-check_item\"><td>2<\/td><td>ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м\/у 1л<\/td><td>79.99<\/td><td>1<\/td><td>79.99<\/td><\/tr><tr class=\"b-check_item\"><td>3<\/td><td>ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м\/у 1л<\/td><td>79.99<\/td><td>1<\/td><td>79.99<\/td><\/tr><tr class=\"b-check_item\"><td>4<\/td><td>*ШАР.Ваф.ВЕН.со взб.сл\/виш.150г<\/td><td>59.99<\/td><td>1<\/td><td>59.99<\/td><\/tr><tr class=\"b-check_item\"><td>5<\/td><td>Вафли ЯШКИНСКИЕ ореховые   300г<\/td><td>94.99<\/td><td>1<\/td><td>94.99<\/td><\/tr><tr class=\"b-check_vblock-first\"><td colspan=\"3\" class=\"b-check_itogo\">ИТОГО:<\/td><td><\/td><td class=\"b-check_itogo\">509.35<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"3\">Наличные<\/td><td><\/td><td>0.00<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"3\">Карта<\/td><td><\/td><td>509.35<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"3\">НДС итога чека со ставкой 20%<\/td><td><\/td><td>15.83<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"3\">НДС итога чека со ставкой 10%<\/td><td><\/td><td>37.66<\/td><\/tr><tr class=\"b-check_vblock-last\"><td colspan=\"5\">ВИД НАЛОГООБЛОЖЕНИЯ: ОСН<\/td><\/tr><tr class=\"b-check_vblock-first\"><td colspan=\"5\">РЕГ.НОМЕР ККТ: 0004000518016307    <\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"5\">ЗАВОД. №: <\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"5\">ФН: 9960440301310853<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"5\">ФД: 77916<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"5\">ФПД#: 147824925<\/td><\/tr><tr class=\"b-check_vblock-last\"><td colspan=\"5\" class=\"b-check_center\"><img src=\"\/qrcode\/generate?text=t%3D20220816T1911%26s%3D509.35%26fn%3D9960440301310853%26i%3D77916%26fp%3D147824925%26n%3D1\" alt=\"QR код чека\" width=\"35%\" loading=\"lazy\" decoding=\"async\"><\/td><\/tr><\/tbody><\/table>"}}'  # noqa: E501
        response.status_code = 200
        fakes.post.return_value = response

        mock_open(
            fakes.product_open,
            read_data=r'{"code":3,"user":"ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ \"АГРОТОРГ\"","items":[{"nds":2,"sum":19439,"name":"Дск Яблоко красное 1кг","price":15999,"quantity":1.215,"paymentType":4,"productType":1,"itemsQuantityMeasure":11},{"nds":2,"sum":7999,"name":"ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м\/у 1л","price":7999,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4607036340658","sernum":"","productIdType":3,"rawProductCode":"4607036340658"}},"itemsQuantityMeasure":0},{"nds":2,"sum":7999,"name":"ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м\/у 1л","price":7999,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4607036340658","sernum":"","productIdType":3,"rawProductCode":"4607036340658"}},"itemsQuantityMeasure":0},{"nds":2,"sum":5999,"name":"*ШАР.Ваф.ВЕН.со взб.сл\/виш.150г","price":5999,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4604386012273","sernum":"","productIdType":3,"rawProductCode":"4604386012273"}},"itemsQuantityMeasure":0},{"nds":1,"sum":9499,"name":"Вафли ЯШКИНСКИЕ ореховые   300г","price":9499,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4607015232646","sernum":"","productIdType":3,"rawProductCode":"4607015232646"}},"itemsQuantityMeasure":0}],"nds10":3766,"nds18":1583,"region":"74","userInn":"7825706086  ","dateTime":"2022-08-16T19:11:00","kktRegId":"0004000518016307    ","metadata":{"id":4373135767659163393,"ofdId":"ofd22","address":"454100,Россия,Челябинская область,Челябинский г.о.,Курчатовский г.п.,Челябинск г,,Новоградский пр-кт,,д. 58,,,,","subtype":"receipt","receiveDate":"2022-08-16T17:13:18Z"},"operator":"Котова Анна Романовна, Продавец-каccир","totalSum":50935,"creditSum":0,"numberKkt":"00105702181010","fiscalSign":147824925,"prepaidSum":0,"retailPlace":"385H; 18300 - Пятерочка;","shiftNumber":302,"cashTotalSum":0,"provisionSum":0,"ecashTotalSum":50935,"operationType":1,"redefine_mask":2,"requestNumber":408,"fiscalDriveNumber":"9960440301310853","messageFiscalSign":9.29735071111385e+18,"retailPlaceAddress":"454000, 74, г.Челябинск, р-н Курчатовский, пр-кт Новоградский, 58;","appliedTaxationType":1,"fiscalDocumentNumber":77916,"fiscalDocumentFormatVer":4}',
            # noqa: E501
        )

        result = process_check(datadir / "foo.jpg")

        assert (
            result
            == r"""Чек некорректен
{"code":0,"first":0,"data":{"json":{"code":3,"user":"ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ \"АГРОТОРГ\"","items":[{"nds":2,"sum":19439,"name":"Дск Яблоко красное 1кг","price":15999,"quantity":1.215,"paymentType":4,"productType":1,"itemsQuantityMeasure":11},{"nds":2,"sum":7999,"name":"ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м\/у 1л","price":7999,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4607036340658","sernum":"","productIdType":3,"rawProductCode":"4607036340658"}},"itemsQuantityMeasure":0},{"nds":2,"sum":7999,"name":"ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м\/у 1л","price":7999,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4607036340658","sernum":"","productIdType":3,"rawProductCode":"4607036340658"}},"itemsQuantityMeasure":0},{"nds":2,"sum":5999,"name":"*ШАР.Ваф.ВЕН.со взб.сл\/виш.150г","price":5999,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4604386012273","sernum":"","productIdType":3,"rawProductCode":"4604386012273"}},"itemsQuantityMeasure":0},{"nds":1,"sum":9499,"name":"Вафли ЯШКИНСКИЕ ореховые   300г","price":9499,"quantity":1,"paymentType":4,"productType":1,"productCodeNew":{"ean13":{"gtin":"4607015232646","sernum":"","productIdType":3,"rawProductCode":"4607015232646"}},"itemsQuantityMeasure":0}],"nds10":3766,"nds18":1583,"region":"74","userInn":"7825706086  ","dateTime":"2022-08-16T19:11:00","kktRegId":"0004000518016307    ","metadata":{"id":4373135767659163393,"ofdId":"ofd22","address":"454100,Россия,Челябинская область,Челябинский г.о.,Курчатовский г.п.,Челябинск г,,Новоградский пр-кт,,д. 58,,,,","subtype":"receipt","receiveDate":"2022-08-16T17:13:18Z"},"operator":"Котова Анна Романовна, Продавец-каccир","totalSum":50935,"creditSum":0,"numberKkt":"00105702181010","fiscalSign":147824925,"prepaidSum":0,"retailPlace":"385H; 18300 - Пятерочка;","shiftNumber":302,"cashTotalSum":0,"provisionSum":0,"ecashTotalSum":50935,"operationType":1,"redefine_mask":2,"requestNumber":408,"fiscalDriveNumber":"9960440301310853","messageFiscalSign":9.29735071111385e+18,"retailPlaceAddress":"454000, 74, г.Челябинск, р-н Курчатовский, пр-кт Новоградский, 58;","appliedTaxationType":1,"fiscalDocumentNumber":77916,"fiscalDocumentFormatVer":4},"html":"<table class=\"b-check_table table\"><tbody><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ \"АГРОТОРГ\"<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">454000, 74, г.Челябинск, р-н Курчатовский, пр-кт Новоградский, 58;<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">ИНН 7825706086  <\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">&nbsp;<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">16.08.2022 19:11<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">Чек № 408<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">Смена № 302<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">Кассир Котова Анна Романовна, Продавец-каccир<\/td><\/tr><tr class=\"b-check_vblock-last b-check_center\"><td colspan=\"5\">Приход<\/td><\/tr><tr><td><strong>№<\/strong><\/td><td><strong>Название<\/strong><\/td><td><strong>Цена<\/strong><\/td><td><strong>Кол.<\/strong><\/td><td><strong>Сумма<\/strong><\/td><\/tr><tr class=\"b-check_item\"><td>1<\/td><td>Дск Яблоко красное 1кг<\/td><td>159.99<\/td><td>1.215<\/td><td>194.39<\/td><\/tr><tr class=\"b-check_item\"><td>2<\/td><td>ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м\/у 1л<\/td><td>79.99<\/td><td>1<\/td><td>79.99<\/td><\/tr><tr class=\"b-check_item\"><td>3<\/td><td>ЧЕБАРКУЛЬ Мол.ОТБ.3,8% м\/у 1л<\/td><td>79.99<\/td><td>1<\/td><td>79.99<\/td><\/tr><tr class=\"b-check_item\"><td>4<\/td><td>*ШАР.Ваф.ВЕН.со взб.сл\/виш.150г<\/td><td>59.99<\/td><td>1<\/td><td>59.99<\/td><\/tr><tr class=\"b-check_item\"><td>5<\/td><td>Вафли ЯШКИНСКИЕ ореховые   300г<\/td><td>94.99<\/td><td>1<\/td><td>94.99<\/td><\/tr><tr class=\"b-check_vblock-first\"><td colspan=\"3\" class=\"b-check_itogo\">ИТОГО:<\/td><td><\/td><td class=\"b-check_itogo\">509.35<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"3\">Наличные<\/td><td><\/td><td>0.00<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"3\">Карта<\/td><td><\/td><td>509.35<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"3\">НДС итога чека со ставкой 20%<\/td><td><\/td><td>15.83<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"3\">НДС итога чека со ставкой 10%<\/td><td><\/td><td>37.66<\/td><\/tr><tr class=\"b-check_vblock-last\"><td colspan=\"5\">ВИД НАЛОГООБЛОЖЕНИЯ: ОСН<\/td><\/tr><tr class=\"b-check_vblock-first\"><td colspan=\"5\">РЕГ.НОМЕР ККТ: 0004000518016307    <\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"5\">ЗАВОД. №: <\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"5\">ФН: 9960440301310853<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"5\">ФД: 77916<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"5\">ФПД#: 147824925<\/td><\/tr><tr class=\"b-check_vblock-last\"><td colspan=\"5\" class=\"b-check_center\"><img src=\"\/qrcode\/generate?text=t%3D20220816T1911%26s%3D509.35%26fn%3D9960440301310853%26i%3D77916%26fp%3D147824925%26n%3D1\" alt=\"QR код чека\" width=\"35%\" loading=\"lazy\" decoding=\"async\"><\/td><\/tr><\/tbody><\/table>"}}"""
            # noqa: E501
        )

        assert fakes.mock_calls == [
            call.check_extractor_open(datadir / "foo.jpg", "rb"),
            call.post(
                "https://proverkacheka.com/api/v1/check/get", data={"token": "prov-check-token"}, files={"qrfile": ANY}
            ),
        ]

    def test_process_json(self, fakes, datadir):
        mock_open(fakes.product_open, read_data=open(datadir / "test_process_json/check_type_2.json", "r").read())

        result = process_check(datadir / "check_type_2.json")

        assert (
            result
            == """1. PAMPERS Premium Care Трусики-Подгуз 4 9-15кг 
2. MATTEL BARBIE Бальзам для губ 2,5 гр:8/288
3. Набор бусин в асс-те (СИ):6/72
4. Пакет подарочный бумажный AB (МакПейпер)"""  # noqa: W291
        )

        assert fakes.mock_calls == [
            call.product_open(str(datadir / "check_type_2.json"), "r", encoding="utf-8"),
            call.product_open().__enter__(),
            call.product_open().read(),
            call.product_open().__exit__(None, None, None),
            call.copy(datadir / "check_type_2.json", datadir / "check_type_2.orig.json"),
            call.reformat_json(datadir / "check_type_2.json", datadir / "check_type_2.reformat.json"),
            call.save_to_google_sheet(
                "creds.json",
                "money-id",
                ProductConfig(
                    name_column="I",
                    quantity_column="K",
                    price_column="L",
                    seller_column="N",
                    category_column="J",
                    date_column="O",
                    current_products_column=9,
                ),
            ),
        ]


class TestSettings:
    @pytest.fixture()
    def mocks(self, mocker):
        open_mock: MagicMock = mocker.patch("bot.settings.open")

        fakes = MagicMock()
        fakes.attach_mock(open_mock, "open")

        return fakes

    def test_save_api(self, mocks, datadir):
        settings = Settings()
        settings.save()

        assert mocks.mock_calls == [
            call.open(ANY, "w+"),
            call.open().__enter__(),
            call.open().__enter__().write(open(datadir / "test_save/1.json").read()),
            call.open().__exit__(None, None, None),
        ]

    def test_load_api(self, mocks, datadir):
        mock_open(mocks.open, read_data=open(datadir / "test_save/1.json").read())

        settings = Settings.load()
        assert settings.extract_method == ExtractMethod.Api

        assert mocks.mock_calls == [
            call.open(ANY, "r"),
            call.open().__enter__(),
            call.open().read(),
            call.open().__exit__(None, None, None),
        ]

    def test_save_selenium(self, mocks, datadir):
        settings = Settings(ExtractMethod.Selenium)
        settings.save()

        assert mocks.mock_calls == [
            call.open(ANY, "w+"),
            call.open().__enter__(),
            call.open().__enter__().write(open(datadir / "test_save/2.json").read()),
            call.open().__exit__(None, None, None),
        ]

    def test_load_selenium(self, mocks, datadir):
        mock_open(mocks.open, read_data=open(datadir / "test_save/2.json").read())

        settings = Settings.load()
        assert settings.extract_method == ExtractMethod.Selenium

        assert mocks.mock_calls == [
            call.open(ANY, "r"),
            call.open().__enter__(),
            call.open().read(),
            call.open().__exit__(None, None, None),
        ]
