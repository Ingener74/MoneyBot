# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from loguru import logger

from Constants import CREDENTIAL_FILE, purchase_config
from Purchase.Check import Check
from Purchase.Purchase import Purchase

load_dotenv()


def process_expense(json_file_name: str) -> Check:
    check = Check()
    with open(json_file_name, 'r', encoding='utf-8') as file_:
        file_data = file_.read()

        json_data = json.loads(file_data)

        # Достаём место продажи
        if 'retailPlace' not in json_data:
            raise KeyError(f"В файле '{json_file_name}' нет записи о продавце")
        retailPlace = json_data['retailPlace']

        # Достаём дату продажи
        if "dateTime" not in json_data:
            raise KeyError
        date_time = json_data["dateTime"]
        if isinstance(date_time, str):
            date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S")
        elif isinstance(date_time, int):
            date_time = datetime.fromtimestamp(date_time)
        else:
            raise TypeError(f"dateTime '{date_time}' has invalid type")
        today_ = date_time.strftime("%d.%m.%Y")
        # logger.debug(f'Date {today_}')
        page_ = date_time.strftime("%m.%Y")
        # logger.debug(f"Page {page_}")

        check.date = page_

        # Достаём список покупок
        if 'items' not in json_data:
            raise KeyError(f"В файле '{json_file_name}' нет списка покупок")
        items = json_data['items']

        for item in items:
            # Достаём название покупки
            if 'name' not in item:
                raise KeyError("В покупке отсутствует имя")
            name = item['name']

            # Достаём количество покупок или вес или т д
            if 'quantity' not in item:
                raise KeyError("В покупке отсутствует количество")
            quantity = str(item['quantity']).replace('.', ',')

            # Достаём цену, одну единицы покупки, сумма посчитается таблицей
            if 'price' not in item:
                raise KeyError("В покупке отсутствует цена")
            price = str(item['price'] / 100).replace('.', ',')

            check.purchases.append(Purchase(name, quantity, price, retailPlace, today_))

    return check


def find_file(dir_: str, file_name: str) -> Optional[str]:
    """
    Находит файл с file_name в каталоге dir
    :param dir:
    :param file_name:
    :return:
    """
    for root, dirs, files in os.walk(dir_):
        for file_ in files:
            if file_ == file_name:
                return os.path.join(root, file_)
    return None


def main():
    os.makedirs('download', exist_ok=True)

    file_ = find_file('download', 'check.json')
    if file_ is None:
        logger.error("File check.json not found")

    check = process_expense(file_)

    Purchase.save(check.date, check.purchases, purchase_config, CREDENTIAL_FILE, os.environ['MONEY_SPREEDSHEET'])

    os.remove(file_)

    logger.info('Done')


if __name__ == '__main__':
    main()
