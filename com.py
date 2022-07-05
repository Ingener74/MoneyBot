# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import datetime

from loguru import logger

from Purchase.Check import Check
from app import find_file
from Constants import purchase_config, CREDENTIAL_FILE
from Purchase.Purchase import Purchase


def collect_purchases_from_file(file_name: str) -> Check:
    check = Check()

    with open(file_name, 'r', encoding='utf-8') as file_:
        purchase = Purchase()
        for line in file_:

            if line.startswith('ИТОГО'):
                price = line.split('...')
                price_ = price[-1]
                price_ = price_.lstrip('.')
                price_ = price_.rstrip('\n')
                price_ = price_.replace('.', ',')
                purchase.price = price_
                purchase.quantity = '1'

            try:
                date_time = datetime.datetime.strptime(line, "%d/%m/%Y         %H:%M:%S\n")
                purchase.today_ = date_time.strftime("%d.%m.%Y")

                check.date = date_time.strftime("%m.%Y")
            except ValueError:
                pass

            if line.startswith('Получатель: '):
                seller = line[len('Получатель: '):]
                seller = seller.rstrip('\n')
                purchase.seller = seller

            if line.startswith('Назначение перевода: '):
                name = line[len('Назначение перевода: '):]
                name = name.rstrip('\n')
                purchase.name = name

                check.purchases.append(purchase)
                purchase = Purchase()

        return check


def main():
    os.makedirs('download', exist_ok=True)

    file_ = find_file('download', 'com.txt')

    if file_ is None:
        logger.error('File com.txt not found')

    check = collect_purchases_from_file(file_)

    Purchase.save(check.date, check.purchases, purchase_config, CREDENTIAL_FILE, os.environ['MONEY_SPREEDSHEET'])

    os.remove(file_)

    logger.info('Done')


if __name__ == '__main__':
    main()
