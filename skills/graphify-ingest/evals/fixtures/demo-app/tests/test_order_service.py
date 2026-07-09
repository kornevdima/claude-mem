from services.order_service import OrderService

def test_create_order():
    svc = OrderService()
    order = svc.create_order("u1", [{"price": 10, "qty": 2}])
    assert order.status == "new"
