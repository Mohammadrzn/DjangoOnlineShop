from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.test import TestCase

from .models import Order, Carts, CartItems, OrderItems
from product.models import Category, Product
from customers.models import Address


class TestOrder(TestCase):
    """
    Unittest class for testing the creation of Order model and its methods.
    """

    def setUp(self) -> None:
        """
        Set up the models required for testing.
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
        Test the creation of the Order model.
        """
        self.assertEqual(self.order.customer, self.user)
        self.assertNotEqual(self.order.registration_date, now())
        self.assertEqual(self.order.delivery_date, "2023-03-23")
        self.assertEqual(self.order.address, self.address)
        expected_products = [repr(self.product)]
        self.assertQuerysetEqual(self.order.product.all(), expected_products, transform=repr)

    def test__str__order(self):
        """
        Test the __str__ method of the Order model.
        """
        self.assertEqual(str(self.order), self.user.username)


class TestCart(TestCase):
    """
    Unittest class for testing the creation of Cart model and its methods.
    """

    def setUp(self) -> None:
        """
        Set up the models required for testing.
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
        Test the creation of the Cart model.
        """
        self.assertEqual(self.cart.customer, self.user)
        expected_products = [repr(self.product)]
        self.assertQuerysetEqual(self.cart.product.all(), expected_products, transform=repr)

    def test__str__cart(self):
        """
        Test the __str__ method of the Cart model.
        """
        self.assertEqual(str(self.cart), f"{self.user.get_full_name}سبد ")


class TestCartItem(TestCase):
    """
    Unittest class for testing the creation of CartItems model and its methods.
    """

    def setUp(self) -> None:
        """
        Set up the models required for testing.
        """
        self.user = get_user_model().objects.create_user(edited_at=now(), deleted_at=None, password="test_password",
                                                         username="test_username", role="C")
        self.category = Category.objects.create(name="test", created_at=now(), edited_at=now(), deleted_at=None)
        self.product = Product.objects.create(category=self.category, name="test", price=120.5, count=5, brand="test",
                                              description="test")
        self.cart = Carts.objects.create(customer=self.user)
        self.cart.product.set([self.product], through_defaults={'count': 1})
        self.products = self.cart.product.filter(id=self.product.id).exists()
        self.cart_items = CartItems.objects.create(cart=self.cart, count=7, product=self.product)

    def test_create_cartItems(self):
        """
        Test the creation of the CartItems model.
        """
        self.assertEqual(self.cart_items.cart, self.cart)
        self.assertEqual(self.cart_items.count, 7)
        self.assertEqual(self.cart_items.product, self.product)

    def test__str__cartItems(self):
        """
        Test the __str__ method of the CartItems model.
        """
        self.assertEqual(str(self.cart_items), self.product.name)
