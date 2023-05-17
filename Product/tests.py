from django.test import TestCase
from .models import Category


class CategoryTest(TestCase):

    def setUp(self) -> None:
        self.category = Category(name="test")

    def test_create_category(self):
        self.assertEqual(self.category.name, "test")
        self.assertFalse(self.category.is_deleted)
