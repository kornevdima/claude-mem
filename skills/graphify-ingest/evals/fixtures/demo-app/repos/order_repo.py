from utils.db import get_connection

class OrderRepo:
    def save(self, order):
        with get_connection() as conn:
            conn.execute("INSERT INTO orders ...", order.__dict__)

    def get(self, order_id):
        with get_connection() as conn:
            return conn.query_one("SELECT * FROM orders WHERE id=?", order_id)

    def mark_cancelled(self, order_id):
        with get_connection() as conn:
            conn.execute("UPDATE orders SET status='cancelled' WHERE id=?", order_id)
