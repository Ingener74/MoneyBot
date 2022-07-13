from dataclasses import dataclass


@dataclass()
class Product:
    name: str = ""
    quantity: float = 0.0
    price: float = 0.0
    seller: str = ""

    @property
    def quantity_(self) -> str:
        q = str(self.quantity)
        return q.replace(".", ",")

    @property
    def price_(self) -> str:
        p = str(self.price)
        return p.replace(".", ",")
