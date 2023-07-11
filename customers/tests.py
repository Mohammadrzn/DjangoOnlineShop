from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.test import TestCase

from .models import Address


class TestUsers(TestCase):
    """
    Unittest class for test creation of Customer model and superuser, and their methods
    """

    def setUp(self) -> None:
        """
        creating the models requirements for testing
        """
        self.user = get_user_model().objects.create_user(edited_at=now(), deleted_at=now(), password="test_password",
                                                         username="test_user_name", first_name="test_first_name",
                                                         last_name="test_last_name", email="test@user.com",
                                                         mobile=9123456789, telephone=66554433,
                                                         national_id="0123456789", age=20, role="A", gender="M")
        self.superuser = get_user_model().objects.create_superuser(username="admin", email="test@admin.com",
                                                                   password="test_password_admin")

    def test_create_user(self):
        """
        test creation of Customer model
        """
        # Running the tests takes some time, so the times will not be equal and will differ by a few milliseconds
        self.assertNotEqual(self.user.edited_at, now())
        self.assertNotEqual(self.user.deleted_at, now())
        self.assertTrue(self.user.password, check_password("test_password", self.user.password))
        self.assertTrue(self.user.is_active)
        self.assertEqual(self.user.username, "test_user_name")
        self.assertEqual(self.user.first_name, "test_first_name")
        self.assertEqual(self.user.last_name, "test_last_name")
        self.assertEqual(self.user.email, "test@user.com")
        self.assertFalse(self.user.is_staff)
        self.assertEqual(self.user.mobile, 9123456789)
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
        self.assertTrue(self.user.password, check_password("test_password_admin", self.user.password))
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
        self.user = get_user_model().objects.create_user(edited_at=now(), deleted_at=now(), password="test_password",
                                                         username="test_username", role="A")
        self.address = Address.objects.create(created_at=now(), edited_at=now(), customer=self.user, state="test_state",
                                              city="test_city", full_address="test_full_address", postal_code=123456789,
                                              is_default=True)

    def test_create_address(self):
        """
        test creation of Address model
        """
        # Running the tests takes some time, so the times will not be equal and will differ by a few milliseconds
        self.assertNotEqual(self.address.created_at, now())
        self.assertNotEqual(self.address.edited_at, now())
        self.assertEqual(self.address.customer, self.user)
        self.assertEqual(self.address.state, "test_state")
        self.assertEqual(self.address.city, "test_city")
        self.assertEqual(self.address.full_address, "test_full_address")
        self.assertEqual(self.address.postal_code, 123456789)
        self.assertTrue(self.address.is_default)

    def test__str__address(self):
        """
        test __str__ method of Address model
        """
        self.assertEqual(str(self.address), str(self.user.id))
