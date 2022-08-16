# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass()
class PurchaseConfig:
    name_column: str
    quantity_column: str
    price_column: str
    seller_column: str
    today_column: str
    category_column: str

    # Номер столбца в котором записаны названия покупок, по ней мы определяем следующую пустую строку
    current_purchases_column: int
