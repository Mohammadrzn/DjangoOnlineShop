from django.test import TestCase
from .models import Order


class TestOrder(TestCase):

    def setUp(self) -> None:
        self.order = Order.objects.create(registration_date="2023-05-18 20:04:49", delivery_date="2023-05-18",
                                          address="test")

    def test_create_order(self):
        self.assertEqual(self.order.registration_date, "2023-05-18 20:04:49")
        self.assertEqual(self.order.delivery_date, "2023-05-18")
        self.assertEqual(self.order.address, "test")
