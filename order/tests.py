from django.contrib.auth import get_user_model
from product.models import Category, Product
from django.utils.timezone import now
from customers.models import Address
from django.test import TestCase
from .models import Order, Carts


class TestOrder(TestCase):
    """
    Unittest class for test creation of order model and it's methods
    """

    def setUp(self) -> None:
        """
        creating the models requirements for testing
        """
        self.user = get_user_model().objects.create_user(edited_at=now(), deleted_at=now(), password="test",
                                                         username="test_username", role="C")
        self.category = Category.objects.create(name="test", created_at=now(), edited_at=now(), deleted_at=now())
        self.product = Product.objects.create(category=self.category, name="test", price=150.5, count=5, brand="test",
                                              description="test")
        self.address = Address.objects.create(created_at=now(), edited_at=now(), customer=self.user, state="test_state",
                                              city="test_city", full_address="test_full_address", postal_code=123456789,
                                              )
        self.order = Order.objects.create(customer=self.user, registration_date=now(), delivery_date="2023-03-23",
                                          address=self.address)
        self.order.product.set([self.product])  # set the product in list (set have to iterate on something) for
        # testing the many-to-many field on order model
        self.products = self.order.product.filter(id=self.product.id).exists()

    def test_create_order(self):
        """
        test creation of order model
        """
        self.assertEqual(self.order.customer, self.user)
        self.assertNotEqual(self.order.registration_date, now())
        self.assertEqual(self.order.delivery_date, "2023-03-23")
        self.assertEqual(self.order.address, self.address)
        expected_products = [repr(self.product)]
        self.assertQuerysetEqual(self.order.product.all(), expected_products, transform=repr)

    def test__str__order(self):
        """
        test __str__ method of order model
        """
        self.assertNotEqual(str(self.order), "test")


class TestCart(TestCase):
    """
    Unittest class for test creation of cart model and it's methods
    """

    def setUp(self) -> None:
        """
        creating the models requirements for testing
        """
        self.user = get_user_model().objects.create_user(edited_at=now(), deleted_at=now(), password="test_password",
                                                         username="test_username", role="C")
        self.category = Category.objects.create(name="test", created_at=now(), edited_at=now(), deleted_at=now())
        self.product = Product.objects.create(category=self.category, name="test", price=150.5, count=5, brand="test",
                                              description="test")
        self.cart = Carts.objects.create(customer=self.user)
        self.cart.product.set([self.product], through_defaults={'count': 1})
        self.products = self.cart.product.filter(id=self.product.id).exists()

    def test_creat_cart(self):
        """
        test creation of cart model
        """
        self.assertEqual(self.cart.customer, self.user)
        expected_products = [repr(self.product)]
        self.assertQuerysetEqual(self.cart.product.all(), expected_products, transform=repr)
