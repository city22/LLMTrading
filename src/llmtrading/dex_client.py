from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Order:
    side: str
    base_amount: float
    quote_amount: float
    price: float


@dataclass
class DexClient:
    """A minimalistic, in-memory execution stub for DEX orders."""

    base_symbol: str
    quote_symbol: str
    executed_orders: List[Order] = field(default_factory=list)

    def place_order(self, side: str, base_amount: float, price: float) -> Order:
        """Simulate placing an order and store it in memory."""

        quote_amount = base_amount * price
        order = Order(side=side, base_amount=base_amount, quote_amount=quote_amount, price=price)
        self.executed_orders.append(order)
        return order
