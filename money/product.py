from dataclasses import dataclass
from datetime import date


@dataclass()
class Product:
    name: str = ''
    quantity: float = 0.0
    price: float = 0.0
    seller: str = ''
    date: date = date(2000, 1, 1)

    @property
    def quantity_(self) -> str:
        q = str(self.quantity)
        return q.replace('.', ',')

    @property
    def price_(self) -> str:
        p = str(self.price)
        return p.replace('.', ',')

    @property
    def date_(self) -> str:
        d = self.date.strftime("%d.%m.%Y")
        return d
