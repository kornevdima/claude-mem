"""Demo shop API — fixture for graphify eval suite."""
from services.order_service import OrderService
from services.payment_service import PaymentService

order_service = OrderService()
payment_service = PaymentService()

def route_create_order(request):
    """POST /orders"""
    return order_service.create_order(request["user_id"], request["items"])

def route_refund(request):
    """POST /refunds"""
    return payment_service.refund(request["payment_id"])

def route_health(_request):
    return {"status": "ok"}
