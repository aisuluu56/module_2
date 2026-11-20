from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    product_id: int
    name: str
    category: str
    manufacturer: str
    composition: str
    image: Optional[str]
    price: float
    quantity: int
    had_orders_last_month: bool

    DISCOUNT_RATE = 0.25

    @property
    def has_discount(self) -> bool:
        return not self.had_orders_last_month

    @property
    def final_price(self) -> float:
        if self.has_discount:
            return round(self.price * (1 - self.DISCOUNT_RATE), 2)
        return round(self.price, 2)