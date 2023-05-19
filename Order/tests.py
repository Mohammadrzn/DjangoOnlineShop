from datetime import datetime
from django.test import TestCase
from .models import Order, Customer


class TestOrder(TestCase):

    def setUp(self) -> None:
        self.user = Customer.objects.create(password="test", username="test",
                                            first_name="test_first_name",
                                            last_name="test_last_name", email="test@user.com",
                                            mobile="9123456789",
                                            national_id="0123456789", age=19, gender="M",
                                            telephone=66554433)
        self.order = Order.objects.create(customer=self.user, registration_date=datetime.now,
                                          delivery_date="2023-05-18",
                                          address="test")

    def test_create_order(self):
        self.assertEqual(self.order.customer, self.user)
        # current_time = datetime.now()
        # formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        # expected_reg_date = datetime.strptime(formatted_time, "%Y-%m-%d %H:%M:%S")
        # self.assertEqual(self.order.registration_date, expected_reg_date)
        self.assertEqual(self.order.delivery_date, "2023-05-18")
        self.assertEqual(self.order.address, "test")
