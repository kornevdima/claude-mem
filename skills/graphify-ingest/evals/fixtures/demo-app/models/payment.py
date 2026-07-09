from dataclasses import dataclass

@dataclass
class Payment:
    amount: float
    currency: str
    auth_id: str
    user_id: str = ""
    status: str = "captured"
