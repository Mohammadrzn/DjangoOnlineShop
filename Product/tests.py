from django.test import TestCase
from .models import Category, Product, Comment


class CategoryTest(TestCase):

    def setUp(self) -> None:
        self.category = Category.objects.create(name="test", upper_category=self.category)
        self.product = Product.objects.create(name="test", price=150.5, count=5, brand="test", description="test")
        self.comment = Comment.objects.create(title="test", content="test & test")

    def test_create_category(self):
        self.assertEqual(self.category.name, "test")
        self.assertEqual(self.category.upper_category, self.category)
        self.assertFalse(self.category.is_deleted)

    def test_create_product(self):
        self.assertEqual(self.product.name, "test")
        self.assertEqual(self.product.price, 150.5)
        self.assertEqual(self.product.count, 5)
        self.assertEqual(self.product.brand, "test")
        self.assertEqual(self.product.description, "test")

    def test_create_comment(self):
        self.assertEqual(self.product.title, "test")
        self.assertEqual(self.product.content, "test & test")

    def test_str_category(self):
        self.assertNotEqual(str(self.category), "not_test")

    def test_str_product(self):
        self.assertNotEqual(str(self.product), "not_test")

    def test_str_comment(self):
        self.assertNotEqual(str(self.comment), "not_test")
