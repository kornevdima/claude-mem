from utils.email import EmailSender

class Notifier:
    def __init__(self):
        self.email = EmailSender()

    def order_confirmation(self, order, payment):
        body = f"Order {order.order_id} confirmed, paid {payment.amount}"
        self.email.send_email(order.user_id, "Order confirmed", body)

    def refund_notice(self, payment):
        self.email.send_email(payment.user_id, "Refund processed", str(payment.amount))
