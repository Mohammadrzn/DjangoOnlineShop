from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.test import TestCase

from .models import Category, Product, Comment


class CategoryTest(TestCase):
    """
    class for test creation of Category model and it's methods
    """

    def setUp(self) -> None:
        """
        creating the models requirements for testing
        """
        self.user = get_user_model().objects.create_user(edited_at=now(), deleted_at=now(), password="test",
                                                         username="test_user_name", role="A")
        self.category = Category.objects.create(name="test", created_at=now(), edited_at=now(), deleted_at=now())

    def test_create_category(self):
        """
        test creation of Category model
        """
        self.assertNotEqual(self.category.edited_at, now())
        self.assertNotEqual(self.category.deleted_at, now())
        self.assertEqual(self.category.name, "test")
        self.assertFalse(self.category.is_deleted)

    def test__str__category(self):
        """
        test __str__ method of Category model
        """
        self.assertNotEqual(str(self.category), "not_test")


class TestProduct(TestCase):
    """
    class for test creation of product model and it's methods
    """

    def setUp(self) -> None:
        """
        creating the models requirements for testing
        """
        self.category = Category.objects.create(name="test", created_at=now(), edited_at=now(), deleted_at=now())
        self.product = Product.objects.create(category=self.category, name="test", price=150.5, count=5, brand="test",
                                              description="test")

    def test_create_product(self):
        """
        test creation of product model
        """
        self.assertNotEqual(self.product.edited_at, now())
        self.assertNotEqual(self.product.deleted_at, now())
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.name, "test")
        self.assertEqual(self.product.price, 150.5)
        self.assertEqual(self.product.count, 5)
        self.assertEqual(self.product.brand, "test")
        self.assertEqual(self.product.description, "test")

    def test__str__product(self):
        """
        test __str__ method of product model
        """
        self.assertNotEqual(str(self.product), "not_test")


class TestComment(TestCase):
    """
    class for test creation of Comment model and it's methods
    """

    def setUp(self) -> None:
        """
        creating the models requirements for testing
        """
        self.user = get_user_model().objects.create_user(edited_at=now(), deleted_at=now(), password="test",
                                                         username="test_user_name", role="A")
        self.category = Category.objects.create(name="test", created_at=now(), edited_at=now(), deleted_at=now())
        self.product = Product.objects.create(category=self.category, name="test", price=150.5, count=5, brand="test",
                                              description="test")
        self.comment = Comment.objects.create(title="test", content="test & test", user=self.user, product=self.product)

    def test_create_comment(self):
        """
        test creation of Comment model
        """
        self.assertNotEqual(self.comment.edited_at, now())
        self.assertNotEqual(self.comment.deleted_at, now())
        self.assertEqual(self.comment.title, "test")
        self.assertEqual(self.comment.content, "test & test")
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.product, self.product)

    def test_str_comment(self):
        """
        test __str__ method of Comment model
        """
        self.assertNotEqual(str(self.comment), "not_test")
