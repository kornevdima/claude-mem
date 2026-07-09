from dataclasses import dataclass, field

@dataclass
class Order:
    user_id: str
    items: list
    order_id: str = "generated"
    payment_id: str = ""
    status: str = "new"

    def total(self):
        return sum(i.get("price", 0) * i.get("qty", 1) for i in self.items)
