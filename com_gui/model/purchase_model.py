# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from PySide6.QtGui import QStandardItemModel, QStandardItem

from Purchase.Check import Check


def create_model(check: Check):
    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(["Название", "Кол-во", "Цена", "Продавец", "Дата"])
    for purchase in check.purchases:
        model.appendRow(
            [
                QStandardItem(purchase.name),
                QStandardItem(purchase.quantity),
                QStandardItem(purchase.price),
                QStandardItem(purchase.seller),
                QStandardItem(purchase.today_),
            ]
        )

    return model
