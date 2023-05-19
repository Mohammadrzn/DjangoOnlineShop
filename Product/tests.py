from django.test import TestCase
from .models import Category, Product, Comment, Customer


class CategoryTest(TestCase):

    def setUp(self) -> None:
        self.user = Customer.objects.create(password="test", username="test",
                                            first_name="test_first_name",
                                            last_name="test_last_name", email="test@user.com",
                                            mobile="9123456789",
                                            national_id="0123456789", age=19, gender="M",
                                            telephone=66554433)
        self.category = Category.objects.create(name="test")
        self.product = Product.objects.create(category=self.category, name="test", price=150.5, count=5, brand="test",
                                              description="test",
                                              is_sold_out=False)
        self.comment = Comment.objects.create(title="test", content="test & test", user=self.user, product=self.product)

    def test_create_product(self):
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.name, "test")
        self.assertEqual(self.product.price, 150.5)
        self.assertEqual(self.product.count, 5)
        self.assertEqual(self.product.brand, "test")
        self.assertEqual(self.product.description, "test")
        self.assertEqual(self.product.is_sold_out, False)

    def test_create_category(self):
        self.assertEqual(self.category.name, "test")
        self.assertFalse(self.category.is_deleted)

    def test_create_comment(self):
        self.assertEqual(self.comment.title, "test")
        self.assertEqual(self.comment.content, "test & test")
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.product, self.product)
