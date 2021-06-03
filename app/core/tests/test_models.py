from django.test import TestCase
from django.contrib.auth import get_user_model


class UsersModelTests(TestCase):

    def test_create_user_success_with_valid_data(self):
        """Test creating a new User returns Success"""
        email = 'user@zebrands.com'
        password = 'password123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))  # Check if the encrypted password is correct

    def test_create_super_user_success_with_valid_data(self):
        """Test creating a new Super User returns Success"""
        email = 'super_user@zebrands.com'
        password = 'password123'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))  # Check if the encrypted password is correct
        self.assertTrue(user.is_superuser)  # Check if user is Super user
        self.assertTrue(user.is_staff)  # Check if user is Admin

    def test_create_user_success_with_upper_email(self):
        """Test the email of a new user is normalized"""
        email = 'user@ZEBRANDS.COM'
        password = 'password123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_create_user_fails_with_no_email(self):
        """Test creating user with invalid error raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'password123')

    def test_create_user_fails_with_invalid_email(self):
        """Test creating user with invalid error raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('pedro_rodriguez@another.domain', 'password123')
