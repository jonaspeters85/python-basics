from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, PositiveInt, ValidationError


class Item(BaseModel):
    name: str = Field(min_length=1)
    qty: PositiveInt
    unit_price: float = Field(gt=0)


class Order(BaseModel):
    currency: Literal["EUR", "USD"] = "EUR"
    vat_rate: float = Field(ge=0, le=1)
    items: list[Item]

    def net_total(self) -> float:
        return sum(i.qty * i.unit_price for i in self.items)

    def vat_amount(self) -> float:
        return self.net_total() * self.vat_rate

    def gross_total(self) -> float:
        return self.net_total() + self.vat_amount()


def main() -> int:
    path = Path("orders.json")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        order = Order.model_validate(data)
    except FileNotFoundError:
        print("❌ orders.json nicht gefunden (im Projektordner anlegen).")
        return 1
    except (json.JSONDecodeError, ValidationError) as e:
        print("❌ Ungültige Daten in orders.json:")
        print(e)
        return 1

    net = order.net_total()
    vat = order.vat_amount()
    gross = order.gross_total()

    print("✅ Order Summary")
    print(f"Netto:  {net:.2f} {order.currency}")
    print(f"MwSt:   {vat:.2f} {order.currency}  (Rate: {order.vat_rate:.0%})")
    print(f"Brutto: {gross:.2f} {order.currency}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
