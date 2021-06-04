from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient   # To make requests to our API
from rest_framework import status

from user.serializers import UserSerializer

CREATE_USER_URL = reverse('user:create')  # User create URL constant
TOKEN_URL = reverse('user:token')  # User token URL constant
LIST_USERS_URL = reverse('user:list')  # User list URL constant


def unique_user_url(user_id=1):
    """Return product Update URL"""
    return reverse('user:user', args=[user_id])


def create_user(**params):
    """Help function to create a user"""
    return get_user_model().objects.create_user(**params)


class PublicUsersAPITests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        """Initialize Client"""
        self.client = APIClient()

    def test_retrieve_users_fails_when_unauthorized(self):
        """Test that list users fails when user is not authenticated"""
        # First populate the DB with some dummy users
        create_user(email='user1@zebrands.com', password='p111', name='User One')
        create_user(email='user2@zebrands.com', password='p222', name='User Two')

        result = self.client.get(LIST_USERS_URL)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_fails_when_user_unauthorized(self):
        """Test creating a user already exists fails"""
        data = {
            'email': 'test@zebrands.com',
            'password': 'pass123',
            'name': 'User Full Name'
        }

        # Make POST request to create user
        result = self.client.post(CREATE_USER_URL, data)

        # API returns 401 (Unauthorized) status since an anonymous user is not authorized to create users
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        url = unique_user_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test API requests that require authentication"""
    def setUp(self):
        self.user = create_user(
            email='test@zebrands.com',
            password='pass123',
            name='User Full Name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_users_success(self):
        """Test that all users are retrieved for authenticated users"""
        # First populate the DB with some dummy users
        create_user(email='user1@zebrands.com', password='p111', name='User One')
        create_user(email='user2@zebrands.com', password='p222', name='User Two')

        result = self.client.get(LIST_USERS_URL)

        users = get_user_model().objects.all()
        serializer = UserSerializer(users, many=True)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_create_valid_user_success(self):
        """Test creating user with valid data is successful"""
        data = {
            'email': 'new_user@zebrands.com',
            'password': 'pass123',
            'name': 'New User Full Name'
        }

        # Make POST request to create user
        result = self.client.post(CREATE_USER_URL, data)

        # API returns 201 (Created) status
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**result.data)  # Get just created user
        self.assertTrue(user.check_password(data['password']))  # Check password is valid
        self.assertNotIn('password', result.data)   # make sure password is not in the response

    def test_create_user_fails_when_user_already_exists(self):
        """Test creating a user already exists fails"""
        data = {
            'email': 'test@zebrands.com',
            'password': 'pass123',
            'name': 'User Full Name'
        }

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

        response = self.client.post(TOKEN_URL, data)

        # Check that the response does not contain a Token
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_fails_when_user_does_not_exist(self):
        """Test that troken is not created when user does not exist"""
        data = {
            'email': 'inexistent_user@zebrands.com',
            'password': 'pass123'
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

    def test_retrieve_profile_success(self):
        """Test retrieving profile for existent user"""
        url = unique_user_url(self.user.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': self.user.id,
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_not_allowed(self):
        """Test that POST is not allowed on the ME URL (Only PUT)"""
        url = unique_user_url()
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_partial_update_user_profile(self):
        """Test updating the user profile with PATCH for authenticated user"""
        data = {
            'name': 'New Name',
            'password': 'newpassword'
        }

        url = unique_user_url(self.user.id)
        response = self.client.patch(url, data)

        self.user.refresh_from_db()

        self.assertEqual(self.user.name, data['name'])
        self.assertTrue(self.user.check_password(data['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_user_profile(self):
        """Test updating the user profile with PUT for authenticated user"""
        data = {
            'email': 'new_user@zebrands.com',
            'name': 'New Name',
            'password': 'newpassword'
        }

        url = unique_user_url(self.user.id)
        response = self.client.put(url, data)

        self.user.refresh_from_db()

        self.assertEqual(self.user.name, data['name'])
        self.assertEqual(self.user.email, data['email'])
        self.assertTrue(self.user.check_password(data['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_user_profile_fails_with_missing_parameters(self):
        """Test updating the user profile with PUT for authenticated user"""
        data = {
            'name': 'New Name',
            'password': 'newpassword'
        }

        url = unique_user_url(self.user.id)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
