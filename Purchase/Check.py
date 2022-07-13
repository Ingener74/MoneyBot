# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import List

from Purchase.Purchase import Purchase


@dataclass()
class Check:
    purchases: List[Purchase] = field(default_factory=list)
    date: str = ""

    @property
    def purchase_list(self) -> str:
        purchase: Purchase
        return "\n".join([f"{index_}. {purchase.name}" for index_, purchase in enumerate(self.purchases, start=1)])
