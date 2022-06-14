from dataclasses import dataclass, field
from typing import List

from money.product import Product


@dataclass()
class Check:
    goods: List[Product] = field(default_factory=list)
