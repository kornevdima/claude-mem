from repos.order_repo import OrderRepo
from services.payment_service import PaymentService
from services.notification_service import Notifier
from models.order import Order

class OrderService:
    def __init__(self):
        self.repo = OrderRepo()
        self.payments = PaymentService()
        self.notifier = Notifier()

    def create_order(self, user_id, items):
        order = Order(user_id=user_id, items=items)
        self.repo.save(order)
        charge = self.payments.charge(order)
        self.notifier.order_confirmation(order, charge)
        return order

    def cancel_order(self, order_id):
        order = self.repo.get(order_id)
        self.payments.refund(order.payment_id)
        return self.repo.mark_cancelled(order_id)
