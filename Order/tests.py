from django.contrib.auth import get_user_model
from Product.models import Category, Product
from django.utils.timezone import now
from django.test import TestCase
from .models import Order


class TestOrder(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(edited_at=now(), deleted_at=now(), password="test",
                                                         username="test_user_name", role="A")
        self.category = Category.objects.create(name="test", created_at=now(), edited_at=now(), deleted_at=now())
        self.product = Product.objects.create(category=self.category, name="test", price=150.5, count=5, brand="test",
                                              description="test")
        self.order = Order.objects.create(customer=self.user, registration_date=now(), delivery_date="2023-03-23",
                                          address="test")
        self.order.product.set([self.product])
        self.products = self.order.product.filter(id=self.product.id).exists()

    def test_create_order(self):
        self.assertEqual(self.order.customer, self.user)
        self.assertNotEqual(self.order.registration_date, now())
        self.assertEqual(self.order.delivery_date, "2023-03-23")
        self.assertEqual(self.order.address, "test")
        self.assertTrue(self.products)

    def test__str__order(self):
        self.assertNotEqual(str(self.order), "test")
