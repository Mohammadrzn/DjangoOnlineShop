from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.hashers import check_password


class UsersTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(password="test", username="test_user_name",
                                                         first_name="test_first_name", last_name="test_last_name",
                                                         email="test@user.com", mobile=9123456789, telephone=66554433,
                                                         national_id="0123456789", age=20, role="A", gender="M")
        self.superuser = get_user_model().objects.create_superuser(username="admin", email="test@admin.com",
                                                                   password="test")

    def test_create_user(self):
        self.assertTrue(self.user.password, check_password("test", self.user.password))
        self.assertTrue(self.user.is_active)
        self.assertNotEqual(self.user.username, "not_test_user_name")
        self.assertNotEqual(self.user.first_name, "not_test_first_name")
        self.assertNotEqual(self.user.last_name, "not_test_last_name")
        self.assertNotEqual(self.user.email, "not_test@user.com")
        self.assertFalse(self.user.is_staff)
        self.assertNotEqual(self.user.mobile, 9876543219)
        self.assertEqual(self.user.telephone, 66554433)
        self.assertEqual(self.user.national_id, "0123456789")
        self.assertEqual(self.user.age, 20)
        self.assertEqual(self.user.role, "A")
        self.assertEqual(self.user.gender, "M")
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        self.assertEqual(self.superuser.username, "admin")
        self.assertEqual(self.superuser.email, "test@admin.com")
        self.assertTrue(self.user.password, check_password("test", self.user.password))
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)
