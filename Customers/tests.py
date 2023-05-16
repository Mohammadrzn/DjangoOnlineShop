from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(password="test", username="test_user_name",
                                                         first_name="test_first_name",
                                                         last_name="test_last_name", email="test@user.com",
                                                         # mobile="9123456789",
                                                         national_id="0123456789", age=19, gender="M",
                                                         telephone=66554433)
        self.superuser = get_user_model().objects.create_superuser(username="admin", email="test@admin.com",
                                                                   password="test")

    def test_create_user(self):
        self.assertEqual(self.user.password, self.user.password)
        # How to get the encrypted password

        self.assertEqual(self.user.username, "test_user_name")
        self.assertEqual(self.user.first_name, "test_first_name")
        self.assertEqual(self.user.last_name, "test_last_name")
        self.assertEqual(self.user.email, "test@user.com")
        # self.assertEqual(self.user.mobile, "9123456789")
        self.assertEqual(self.user.national_id, "0123456789")
        self.assertEqual(self.user.age, 19)
        self.assertEqual(self.user.gender, "M")
        self.assertEqual(self.user.telephone, 66554433)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        self.assertEqual(self.superuser.username, "admin")
        self.assertEqual(self.superuser.email, "test@admin.com")
        self.assertEqual(self.superuser.password, self.superuser.password)
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)
