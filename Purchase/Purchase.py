# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from typing import List

import gspread

from Purchase.PurchaseConfig import PurchaseConfig


@dataclass
class Purchase:
    name: str = ''
    quantity: str = ''
    price: str = ''
    seller: str = ''
    today_: str = ''

    @staticmethod
    def save(page: str,
             purchases: List[Purchase],
             config: PurchaseConfig,
             service_account_token_file_name: str,
             spreadsheet_id: str):

        if not purchases:
            raise ValueError("Empty purchases list")

        gc = gspread.service_account(filename=service_account_token_file_name)
        sh = gc.open_by_key(spreadsheet_id)
        worksheet = sh.worksheet(page)

        current_purchases = worksheet.col_values(config.current_purchases_column)

        next_row = len(current_purchases) + 1

        num_of_purchases = len(purchases)

        name_data = []
        quantity_data = []
        price_data = []
        seller_data = []
        today_data = []

        for purchase in purchases:
            name_data.append([purchase.name])
            quantity_data.append([purchase.quantity])
            price_data.append([purchase.price])
            seller_data.append([purchase.seller])
            today_data.append([purchase.today_])

        def update_and_format(column, next_row, purchases, data):
            worksheet.update(f"{column}{next_row}:{column}{next_row + purchases}", data,
                             value_input_option='USER_ENTERED')
            worksheet.format(f"{column}{next_row}:{column}{next_row + (purchases - 1)}", {
                "backgroundColor": {
                    "red": 0.76,
                    "green": 0.87,
                    "blue": 0.82
                }
            })

        update_and_format(config.name_column, next_row, num_of_purchases, name_data)
        update_and_format(config.quantity_column, next_row, num_of_purchases, quantity_data)
        update_and_format(config.price_column, next_row, num_of_purchases, price_data)
        update_and_format(config.seller_column, next_row, num_of_purchases, seller_data)
        update_and_format(config.today_column, next_row, num_of_purchases, today_data)
