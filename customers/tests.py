from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.test import TestCase
from .models import Address


class UsersTest(TestCase):
    """
    Unittest class for test creation of Customer model and superuser, and their methods
    """

    def setUp(self) -> None:
        """
        creating the models requirements for testing
        """
        self.user = get_user_model().objects.create_user(edited_at=now(), deleted_at=now(), password="test",
                                                         username="test_user_name", first_name="test_first_name",
                                                         last_name="test_last_name", email="test@user.com",
                                                         mobile=9123456789, telephone=66554433,
                                                         national_id="0123456789", age=20, role="A", gender="M")
        self.superuser = get_user_model().objects.create_superuser(username="admin", email="test@admin.com",
                                                                   password="test")

    def test_create_user(self):
        """
        test creation of Customer model
        """
        self.assertNotEqual(self.user.edited_at, now())
        self.assertNotEqual(self.user.deleted_at, now())
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
        self.assertFalse(self.user.is_deleted)

    def test__str__user(self):
        """
        test __str__ method of Customer model
        """
        self.assertEqual(str(self.user), "test_first_name test_last_name")

    def test_create_superuser(self):
        """
        test creation of superuser
        """
        self.assertEqual(self.superuser.username, "admin")
        self.assertEqual(self.superuser.email, "test@admin.com")
        self.assertTrue(self.user.password, check_password("test", self.user.password))
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)


class TestAddress(TestCase):
    """
    Unittest class for test creation of Address model and it's methods
    """

    def setUp(self) -> None:
        """
        creating the models requirements for testing
        """
        self.user = get_user_model().objects.create_user(edited_at=now(), deleted_at=now(), password="test",
                                                         username="test_user_name", role="A")
        self.address = Address.objects.create(created_at=now(), edited_at=now(), customer=self.user, state="test",
                                              city="test", full_address="test", postal_code=123456789)

    def test_create_address(self):
        """
        test creation of Address model
        """
        self.assertNotEqual(self.address.created_at, now())
        self.assertNotEqual(self.address.edited_at, now())
        self.assertEqual(self.address.customer, self.user)
        self.assertNotEqual(self.address.state, "not_test")
        self.assertNotEqual(self.address.city, "not_test")
        self.assertNotEqual(self.address.full_address, "not_test")
        self.assertNotEqual(self.address.postal_code, 987654321)

    def test__str__address(self):
        """
        test __str__ method of Address model
        """
        self.assertEqual(str(self.address), str(self.user.id))
