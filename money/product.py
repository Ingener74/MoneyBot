from __future__ import annotations

import json
from collections import namedtuple
from dataclasses import dataclass, field
from datetime import date
from datetime import datetime
from typing import List

import gspread


@dataclass()
class ProductConfig:
    name_column: str
    quantity_column: str
    price_column: str
    seller_column: str
    category_column: str
    date_column: str

    # Номер столбца в котором записаны названия покупок, по ней мы определяем следующую пустую строку
    current_products_column: int


@dataclass()
class Product:
    name: str = ""
    quantity: float = 0.0
    price: float = 0.0
    seller: str = ""
    category: str = ""
    date_of_purchase: date = date(2000, 1, 1)

    @property
    def quantity_(self) -> str:
        q = str(self.quantity)
        return q.replace(".", ",")

    @property
    def price_(self) -> str:
        p = str(self.price)
        return p.replace(".", ",")

    @property
    def date_of_purchase_(self) -> str:
        return self.format_day_month_year(self.date_of_purchase)

    @staticmethod
    def format_day_month_year(date_: date):
        return date_.strftime("%d.%m.%Y")

    @staticmethod
    def format_month_year(date_: date):
        return date_.strftime("%m.%Y")


@dataclass()
class Products:
    goods: List[Product] = field(default_factory=list)

    @property
    def numbered_list_of_names(self):
        return "\n".join([f"{index_}. {purchase.name}" for index_, purchase in enumerate(self.goods, start=1)])

    @staticmethod
    def from_communal_payments(com_pay_file_name) -> Products:
        with open(com_pay_file_name, "r", encoding="utf-8") as file:
            check = Products()
            product = Product(quantity=1.0)
            for line in file:
                if line.startswith("ИТОГО"):
                    product.price = float(line.split("...")[-1].lstrip(".").rstrip("\n"))

                try:
                    date_time = datetime.strptime(line, "%d/%m/%Y         %H:%M:%S\n")
                    product.date_of_purchase = date(date_time.year, date_time.month, date_time.day)
                except ValueError:
                    pass

                if line.startswith("Получатель: "):
                    product.seller = line[len("Получатель: ") :].rstrip("\n")

                if line.startswith("Назначение перевода: "):
                    product.name = line[len("Назначение перевода: ") :].rstrip("\n")

                    check.goods.append(product)
                    product = Product(quantity=1.0)

            return check

    @staticmethod
    def from_json(json_file_name: str) -> Products:
        json_data = Products.__data_from_json_file(json_file_name)

        def get(d, key: str, error_msg: str):
            if key not in d:
                raise KeyError(error_msg)
            return d[key]

        date_time = get(
            json_data,
            "dateTime",
            f"В файле '{json_file_name}' нет записи о дате и времени продажи",
        )

        if isinstance(date_time, str):
            date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S")
        elif isinstance(date_time, int):
            date_time = datetime.fromtimestamp(date_time)
        else:
            raise TypeError(f"dateTime '{date_time}' has invalid type")

        retail_place = get(
            json_data,
            "retailPlace",
            f"В файле '{json_file_name}' нет записи о месте продажи",
        )
        user = get(json_data, "user", f"В файле '{json_file_name}' нет записи о продавце")

        return Products(
            [
                Product(
                    get(item, "name", "В покупке отсутствует имя"),
                    float(get(item, "quantity", "В покупке отсутствует количество")),
                    float(get(item, "price", "В покупке отсутствует цена")) / 100,
                    f"{user}, {retail_place}",
                    date_of_purchase=date(date_time.year, date_time.month, date_time.day),
                )
                for item in get(json_data, "items", f"В файле '{json_file_name}' нет списка покупок")
            ]
        )

    @staticmethod
    def from_google_sheet(start_date: date, end_date: date) -> Products:
        ...

    def save_to_google_sheet(self, service_account_token_file_name: str, spreadsheet_id: str, config: ProductConfig):
        if not self.goods:
            raise ValueError("Empty products list")

        gc = gspread.service_account(filename=service_account_token_file_name)
        sh = gc.open_by_key(spreadsheet_id)
        date_set = set([product.date_of_purchase for product in self.goods])
        if len(date_set) != 1:
            raise ValueError("Different dates in products")

        date_list = list(date_set)

        worksheet = sh.worksheet(Product.format_month_year(date_list[0]))

        current_purchases = worksheet.col_values(config.current_products_column)

        next_row = len(current_purchases) + 1

        num_of_purchases = len(self.goods)

        Category = namedtuple("Category", "row, category")

        name_data = []
        quantity_data = []
        price_data = []
        seller_data = []
        today_data = []
        categories = []

        for index, purchase in enumerate(self.goods):
            name_data.append([purchase.name])
            quantity_data.append([purchase.quantity_])
            price_data.append([purchase.price_])
            seller_data.append([purchase.seller])
            today_data.append([purchase.date_of_purchase_])
            if purchase.category != "":
                categories.append(Category(next_row + index, purchase.category))

        def update_and_format(column, next_row, purchases, data):
            worksheet.update(
                f"{column}{next_row}:{column}{next_row + purchases}",
                data,
                value_input_option="USER_ENTERED",
            )
            worksheet.format(
                f"{column}{next_row}:{column}{next_row + (purchases - 1)}",
                {"backgroundColor": {"red": 0.76, "green": 0.87, "blue": 0.82}},
            )

        update_and_format(config.name_column, next_row, num_of_purchases, name_data)
        update_and_format(config.quantity_column, next_row, num_of_purchases, quantity_data)
        update_and_format(config.price_column, next_row, num_of_purchases, price_data)
        update_and_format(config.seller_column, next_row, num_of_purchases, seller_data)
        update_and_format(config.date_column, next_row, num_of_purchases, today_data)

        for category in categories:
            update_and_format(config.category_column, category.row, 1, [[category.category]])

    @staticmethod
    def __data_from_json_file(json_file_name: str):
        with open(json_file_name, "r", encoding="utf-8") as file_:
            json_data = json.loads(file_.read())
            if "retailPlace" in json_data and "user" in json_data and "dateTime" in json_data and "items" in json_data:
                return json_data
            else:
                return json_data[0]["ticket"]["document"]["receipt"]
