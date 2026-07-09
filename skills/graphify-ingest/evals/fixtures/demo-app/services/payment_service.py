from repos.payment_repo import PaymentRepo
from models.payment import Payment
from utils.config import get_setting

class PaymentGateway:
    def authorize(self, amount, currency):
        return {"auth_id": "A1", "amount": amount, "currency": currency}

class PaymentService:
    def __init__(self):
        self.repo = PaymentRepo()
        self.gateway = PaymentGateway()

    def charge(self, order):
        return self.process_payment(order.total(), get_setting("currency"))

    def process_payment(self, amount, currency):
        auth = self.gateway.authorize(amount, currency)
        payment = Payment(amount=amount, currency=currency, auth_id=auth["auth_id"])
        self.repo.save(payment)
        return payment

    def refund(self, payment_id):
        payment = self.repo.get(payment_id)
        payment.status = "refunded"
        self.repo.save(payment)
        return payment
