"""Teaching model: trusted orders, sequential calls, memory only, no real money."""
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Order:
    order_id: str
    sku: str
    amount_ntd: int


@dataclass(frozen=True)
class Receipt:
    order_id: str
    sku: str
    amount_ntd: int
    status: str
    payment_id: str | None = None


@dataclass(frozen=True)
class Attempt:
    order: Order
    key: str
    receipt: Receipt


class PaymentConflict(Exception):
    pass


class Declined(Exception):
    pass


class Checkout:
    def __init__(self, gateway):
        self.gateway = gateway
        self.attempts = {}
        self.key_orders = {}

    def pay(self, order, key):
        # Order is loaded and authorised by the server before this boundary.
        if not key:
            raise PaymentConflict("an idempotency key is required")
        if key in self.key_orders and self.key_orders[key] != order.order_id:
            raise PaymentConflict("key belongs to another order")
        if order.order_id in self.attempts:
            existing = self.attempts[order.order_id]
            if existing.key != key or existing.order != order:
                raise PaymentConflict("payment attempt cannot be rebound")
            return existing.receipt

        receipt = Receipt(order.order_id, order.sku, order.amount_ntd, "PENDING")
        self.key_orders[key] = order.order_id
        self.attempts[order.order_id] = Attempt(order, key, receipt)
        try:
            payment_id = self.gateway.charge(order.order_id, order.amount_ntd)
        except Declined:
            receipt = replace(receipt, status="DECLINED")
        except TimeoutError:
            receipt = replace(receipt, status="PENDING")
        else:
            receipt = replace(receipt, status="PAID", payment_id=payment_id)
        self.attempts[order.order_id] = Attempt(order, key, receipt)
        return receipt
