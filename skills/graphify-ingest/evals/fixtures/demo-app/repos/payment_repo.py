from utils.db import get_connection

class PaymentRepo:
    def save(self, payment):
        with get_connection() as conn:
            conn.execute("INSERT INTO payments ...", payment.__dict__)

    def get(self, payment_id):
        with get_connection() as conn:
            return conn.query_one("SELECT * FROM payments WHERE id=?", payment_id)
