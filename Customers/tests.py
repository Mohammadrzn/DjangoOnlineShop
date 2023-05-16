from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersTest(TestCase):

    def test_create_user(self):
        user = get_user_model().objects.create_user(password="test", username="test_user_name",
                                                    first_name="test_first_name",
                                                    last_name="test_last_name", email="test@user.com",
                                                    # mobile="9123456789",
                                                    national_id="0123456789", age=19, gender="M", telephone=66554433)

        self.assertEqual(user.password, user.password)
        # How to get the encrypted password

        self.assertEqual(user.username, "test_user_name")
        self.assertEqual(user.first_name, "test_first_name")
        self.assertEqual(user.last_name, "test_last_name")
        self.assertEqual(user.email, "test@user.com")
        # self.assertEqual(user.mobile, "9123456789")
        self.assertEqual(user.national_id, "0123456789")
        self.assertEqual(user.age, 19)
        self.assertEqual(user.gender, "M")
        self.assertEqual(user.telephone, 66554433)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = get_user_model().objects.create_superuser(username="admin", email="test@admin.com", password="test")
        self.assertEqual(superuser.username, "admin")
        self.assertEqual(superuser.email, "test@admin.com")
        self.assertEqual(superuser.password, superuser.password)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
