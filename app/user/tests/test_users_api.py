from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient   # To make requests to our API
from rest_framework import status

CREATE_USER_URL = reverse('user:create')  # User create URL constant
TOKEN_URL = reverse('user:token')  # User token URL constant


def create_user(**params):
    """Help function to create a user"""
    return get_user_model().objects.create_user(**params)


class PublicUsersAPITests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        """Initialize Client"""
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid data is successful"""
        data = {
            'email': 'test@zebrands.com',
            'password': 'pass123',
            'name': 'User Full Name'
        }

        # Make POST request to create user
        result = self.client.post(CREATE_USER_URL, data)

        # API returns 201 (Created) status
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**result.data)  # Get just created user
        self.assertTrue(user.check_password(data['password']))  # Check password is valid

    def test_create_user_fails_when_user_already_exists(self):
        """Test creating a user already exists fails"""
        data = {
            'email': 'test@zebrands.com',
            'password': 'pass123',
            'name': 'User Full Name'
        }
        create_user(**data)

        # Make POST request to create user
        result = self.client.post(CREATE_USER_URL, data)

        # API returns 400 (Bad Request) status since the user already exist
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_success(self):
        """ Test that a token is successfuly created for an existent user"""
        data = {
            'email': 'test@zebrands.com',
            'password': 'pass123'
        }
        create_user(**data)

        response = self.client.post(TOKEN_URL, data)

        # Check that the response contains a Token
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_fails_when_invalid_credentials(self):
        """Test that token is not created when invalid credentials"""
        data = {
            'email': 'test@zebrands.com',
            'password': 'wrong-password'
        }
        create_user(
            email='test@zebrands.com',
            password='pass123'
        )
        response = self.client.post(TOKEN_URL, data)

        # Check that the response does not contain a Token
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_fails_when_user_does_not_exist(self):
        """Test that troken is not created when user does not exist"""
        data = {
            'email': 'test@zebrands.com',
            'password': 'wrong-password'
        }
        response = self.client.post(TOKEN_URL, data)

        # Check that the response does not contain a Token
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_fails_when_missing_field(self):
        """Test that troken is not created when missing field"""
        data = {
            'email': 'test@zebrands.com',
            'password': ''
        }
        response = self.client.post(TOKEN_URL, data)

        # Check that the response does not contain a Token
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
