from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List

from money.product import Product


@dataclass()
class Check:
    goods: List[Product] = field(default_factory=list)
    date: date = date(2000, 1, 1)

    @property
    def date_(self) -> str:
        return self.date.strftime("%d.%m.%Y")

    @staticmethod
    def from_json(json_file_name: str) -> Check:
        json_data = Check.__data_from_json_file(json_file_name)

        def get(d, key: str, error_msg: str):
            if key not in d:
                raise KeyError(error_msg)
            return d[key]

        date_time = get(json_data, "dateTime", f"В файле '{json_file_name}' нет записи о дате и времени продажи")

        if isinstance(date_time, str):
            date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S")
        elif isinstance(date_time, int):
            date_time = datetime.fromtimestamp(date_time)
        else:
            raise TypeError(f"dateTime '{date_time}' has invalid type")

        retail_place = get(json_data, 'retailPlace', f"В файле '{json_file_name}' нет записи о месте продажи")
        user = get(json_data, 'user', f"В файле '{json_file_name}' нет записи о продавце")

        return Check(
            [Product(
                get(item, 'name', "В покупке отсутствует имя"),
                float(get(item, 'quantity', "В покупке отсутствует количество")),
                float(get(item, 'price', "В покупке отсутствует цена")) / 100,
                f"{user}, {retail_place}"
            ) for item in get(json_data, 'items', f"В файле '{json_file_name}' нет списка покупок")],
            date(date_time.year, date_time.month, date_time.day))


    @staticmethod
    def __data_from_json_file(json_file_name: str):
        with open(json_file_name, 'r', encoding='utf-8') as file_:
            json_data = json.loads(file_.read())
            if 'retailPlace' in json_data and 'user' in json_data and 'dateTime' in json_data and 'items' in json_data:
                return json_data
            else:
                return json_data[0]['ticket']['document']['receipt']
