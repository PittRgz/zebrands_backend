from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        """SetUp function for our tests class"""
        self.client = Client()  # Initialize client to make requests
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@zebrands.com',
            password='pasword123'
        )
        self.client.force_login(self.admin_user)  # Force admin user to login
        self.user = get_user_model().objects.create_user(
            email='user@zebrands.com',
            password='pasword123',
            name='User Full Name'
        )

    def test_list_users(self):
        """Test listing users"""
        url = reverse('admin:core_user_changelist')  # Defualt URL
        response = self.client.get(url)  # GET user list

        self.assertContains(response, self.user.name)  # Check for content in the response
        self.assertContains(response, self.user.email)  # Check for content in the response

    def test_edit_users_page_loads_successfully(self):
        """Test edit user page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])  # Defualt URL
        response = self.client.get(url)  # GET user edit page by its ID

        self.assertEqual(response.status_code, 200)  # Ok Status

    def test_create_users_page_loads_successfully(self):
        """Test create user page works"""
        url = reverse('admin:core_user_add')  # Defualt URL
        response = self.client.get(url)  # GET user add page

        self.assertEqual(response.status_code, 200)  # Ok Status
