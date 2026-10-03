"""Approved requirements, not expected values copied from the implementation."""
from dataclasses import replace
import unittest

from payment import Checkout, Declined, Order, PaymentConflict


def tea_order(order_id="tea-001"):
    # Fixture represents a trusted server-side order. NTD 35 is illustrative.
    return Order(order_id, "UNSWEETENED_PURE_GREEN_TEA", 35)


class FakeGateway:
    """Records observable attempts/captures; deliberately does not deduplicate."""
    def __init__(self, outcome="captured"):
        if outcome not in {"captured", "declined", "timeout_before_capture",
                           "timeout_after_capture", "error_after_capture"}:
            raise ValueError(outcome)
        self.outcome = outcome
        self.calls = []
        self.captures = []

    def charge(self, order_id, amount_ntd):
        self.calls.append((order_id, amount_ntd))
        if self.outcome == "declined":
            raise Declined("issuer declined")
        if self.outcome == "timeout_before_capture":
            raise TimeoutError("request did not reach the provider")
        payment_id = f"pay-{len(self.captures) + 1}"
        self.captures.append((payment_id, order_id, amount_ntd))
        if self.outcome == "timeout_after_capture":
            raise TimeoutError("response lost after provider captured payment")
        if self.outcome == "error_after_capture":
            raise ConnectionError("connection reset after capture")
        return payment_id


class FunctionalTests(unittest.TestCase):
    def test_receipt_preserves_purchased_tea(self):
        receipt = Checkout(FakeGateway()).pay(tea_order(), "buy-tea-001")
        self.assertEqual(receipt.status, "PAID")
        self.assertEqual(receipt.order_id, "tea-001")
        self.assertEqual(receipt.sku, "UNSWEETENED_PURE_GREEN_TEA")
        self.assertEqual(receipt.amount_ntd, 35)
        self.assertEqual(receipt.payment_id, "pay-1")

    def test_provider_captures_exactly_35_ntd(self):
        gateway = FakeGateway()
        Checkout(gateway).pay(tea_order(), "buy-tea-001")
        self.assertEqual(gateway.calls, [("tea-001", 35)])
        self.assertEqual(gateway.captures, [("pay-1", "tea-001", 35)])


class ConstraintTests(unittest.TestCase):
    def test_same_attempt_is_not_charged_twice(self):
        gateway = FakeGateway()
        checkout = Checkout(gateway)
        first = checkout.pay(tea_order(), "buy-tea-001")
        second = checkout.pay(tea_order(), "buy-tea-001")
        self.assertEqual(second, first)
        self.assertEqual(gateway.calls, [("tea-001", 35)])
        self.assertEqual(gateway.captures, [("pay-1", "tea-001", 35)])

    def test_key_cannot_move_to_another_order(self):
        gateway = FakeGateway()
        checkout = Checkout(gateway)
        checkout.pay(tea_order(), "buy-tea-001")
        with self.assertRaises(PaymentConflict):
            checkout.pay(tea_order("tea-002"), "buy-tea-001")
        self.assertEqual(gateway.calls, [("tea-001", 35)])

    def test_new_key_cannot_restart_the_same_order(self):
        gateway = FakeGateway()
        checkout = Checkout(gateway)
        checkout.pay(tea_order(), "buy-tea-001")
        with self.assertRaises(PaymentConflict):
            checkout.pay(tea_order(), "new-key")
        self.assertEqual(gateway.calls, [("tea-001", 35)])

    def test_order_contents_cannot_change_during_replay(self):
        gateway = FakeGateway()
        checkout = Checkout(gateway)
        order = tea_order()
        checkout.pay(order, "buy-tea-001")
        for changed in (replace(order, amount_ntd=1),
                        replace(order, sku="SWEETENED_GREEN_TEA")):
            with self.subTest(order=changed):
                with self.assertRaises(PaymentConflict):
                    checkout.pay(changed, "buy-tea-001")
        self.assertEqual(gateway.calls, [("tea-001", 35)])

    def test_declined_payment_is_not_paid(self):
        gateway = FakeGateway("declined")
        checkout = Checkout(gateway)
        receipt = checkout.pay(tea_order(), "buy-tea-001")
        replay = checkout.pay(tea_order(), "buy-tea-001")
        self.assertEqual(receipt.status, "DECLINED")
        self.assertIsNone(receipt.payment_id)
        self.assertEqual(replay, receipt)
        self.assertEqual(gateway.calls, [("tea-001", 35)])
        self.assertEqual(gateway.captures, [])  # Fixture check, not provider evidence.

    def test_timeout_stays_pending_without_another_charge(self):
        for outcome in ("timeout_before_capture", "timeout_after_capture"):
            with self.subTest(outcome=outcome):
                gateway = FakeGateway(outcome)
                checkout = Checkout(gateway)
                first = checkout.pay(tea_order(), "buy-tea-001")
                second = checkout.pay(tea_order(), "buy-tea-001")
                self.assertEqual(first.status, "PENDING")
                self.assertIsNone(first.payment_id)
                self.assertEqual(second, first)
                self.assertEqual(gateway.calls, [("tea-001", 35)])
                expected = [] if outcome == "timeout_before_capture" else [("pay-1", "tea-001", 35)]
                self.assertEqual(gateway.captures, expected)

    def test_unexpected_provider_error_preserves_pending_attempt(self):
        gateway = FakeGateway("error_after_capture")
        checkout = Checkout(gateway)
        with self.assertRaises(ConnectionError):
            checkout.pay(tea_order(), "buy-tea-001")
        try:
            second = checkout.pay(tea_order(), "buy-tea-001")
        except ConnectionError:
            self.fail("replay called the provider again instead of returning PENDING")
        self.assertEqual(second.status, "PENDING")
        self.assertIsNone(second.payment_id)
        self.assertEqual(gateway.calls, [("tea-001", 35)])
        self.assertEqual(gateway.captures, [("pay-1", "tea-001", 35)])


if __name__ == "__main__":
    unittest.main()
