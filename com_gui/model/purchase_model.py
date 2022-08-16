# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from PySide6.QtGui import QStandardItemModel, QStandardItem

from money.product import Products


def create_model(check: Products):
    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(["Название", "Кол-во", "Цена", "Продавец", "Дата"])
    for purchase in check.goods:
        model.appendRow(
            [
                QStandardItem(purchase.name),
                QStandardItem(purchase.quantity_),
                QStandardItem(purchase.price_),
                QStandardItem(purchase.seller),
                QStandardItem(purchase.date_of_purchase_),
            ]
        )

    return model
