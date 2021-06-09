from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from unittest import mock

from core.models import Brand

from brands.serializers import BrandSerializer

LIST_BRANDS_URL = reverse('brands:list')
CREATE_BRAND_URL = reverse('brands:create')


def unique_brand_url(brand_id):
    """Return brand manage URL"""
    return reverse('brands:brand', args=[brand_id])


class PublicBrandsAPITests(TestCase):
    """Test the publicly available Brands API (There are no public APIs for Brands)"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_brands_fails_when_unauthorized(self):
        """Test retrieve brands when unauthorized user"""
        # First populate the DB with some dummy brands
        Brand.objects.create(name='Brand Test Name', category='Test Category')
        Brand.objects.create(name='Brand Test Second Name', category='Test Category 2')

        result = self.client.get(LIST_BRANDS_URL)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_brand_fails_when_unauthorized(self):
        """Test create brand when unauthorized user"""
        data = {
            'name': 'Test Name',
            'category': 'Test Category',
        }

        result = self.client.post(CREATE_BRAND_URL, data)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_brand_fails_when_unauthorized(self):
        """Test edit brand with PATCH when unauthorized user"""
        data = {
            'name': 'Test Name',
        }

        result = self.client.patch(CREATE_BRAND_URL, data)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_full_update_brand_fails_when_unauthorized(self):
        """Test edit brand with PUT when unauthorized user"""
        data = {
            'name': 'Test Name',
            'category': 'Test Category',
        }

        result = self.client.put(CREATE_BRAND_URL, data)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_brand_fails_when_unauthorized(self):
        """Test edit brand with PUT when unauthorized user"""
        # Create a dummy brand
        brand = Brand.objects.create(name='Brand Test Name', category='Test Category')

        url = unique_brand_url(brand.id)
        result = self.client.delete(url)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBrandsAPITests(TestCase):
    """Test the private available Brands API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'user@zebrands.com',
            'pass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_brands_success(self):
        """Test that all brands are retrieved for anyusers"""
        # First populate the DB with some dummy brands
        Brand.objects.create(name='Brand Test Name', category='Test Category')
        Brand.objects.create(name='Brand Test Second Name', category='Test Category 2')

        result = self.client.get(LIST_BRANDS_URL)

        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_create_brand_success(self):
        """Test that a brand is created successfully"""
        data = {
            'name': 'Test Name',
            'category': 'Test Category',
        }

        self.client.post(CREATE_BRAND_URL, data)

        # Check if the created Brand exists
        exists = Brand.objects.filter(
            name=data['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_brand_fails_when_name_already_exists(self):
        """Test that a brand is not created if the SKU already exist"""
        data = {
            'name': 'Test Name',
            'category': 'Test Category',
        }

        # Create a brand with name = Test Name
        Brand.objects.create(name='Test Name', category='Test Category')

        response = self.client.post(CREATE_BRAND_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_brand_fails_with_unvalid_data(self):
        """Test creating a new brand with invalid data"""
        data = {
            'name': '',
            'category': 'Test Category',
        }

        result = self.client.post(CREATE_BRAND_URL, data)

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_parcial_update_brand_success(self):
        """Test updating a brand with PATCH"""
        # Create a dummy brand
        brand = Brand.objects.create(name='Brand Test Name', category='Test Category')

        data = {
            'name': 'New Name',
        }
        url = unique_brand_url(brand.id)
        self.client.patch(url, data)

        brand.refresh_from_db()  # Refresh the brand from the DB

        # Check if name and brand were successfully updated
        self.assertEqual(brand.name, data['name'])

    def test_partial_update_brand_fails_when_invalid_brand_id(self):
        """Test updating a brand with PATCH but invalid brand_id"""
        # Create a dummy brand
        Brand.objects.create(name='Brand Test Name', category='Test Category')

        data = {
            'name': 'New Name',
        }
        url = unique_brand_url(2)
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_full_update_brand_success(self):
        """Test updating a brand with PUT"""
        # Create a dummy brand
        brand = Brand.objects.create(name='Brand Test Name', category='Test Category')

        data = {
            'name': 'New Name',
            'category': 'New Category'
        }
        url = unique_brand_url(brand.id)
        self.client.put(url, data)

        brand.refresh_from_db()  # Refresh the brand from the DB

        # Check if name and brand were successfully updated
        self.assertEqual(brand.name, data['name'])
        self.assertEqual(brand.category, data['category'])

    def test_full_update_brand_fails_when_missing_parameters(self):
        """Test updating a brand with PUT but missing parameters"""
        # Create a dummy brand
        brand = Brand.objects.create(name='Brand Test Name', category='Test Category')

        data = {
            'name': 'New Name',
        }
        url = unique_brand_url(brand.id)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_full_update_brand_fails_when_invalid_brand_id(self):
        """Test updating a brand with PUT but invalid brand_id"""
        # Create a dummy brand
        Brand.objects.create(name='Brand Test Name', category='Test Category')

        data = {
            'name': 'New Name',
            'category': 'New Category'
        }
        url = unique_brand_url(2)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_brand_success(self):
        """Test deleting a brand"""
        # Create a dummy brand
        brand = Brand.objects.create(name='Brand Test Name', category='Test Category')

        url = unique_brand_url(brand.id)
        self.client.delete(url)

        brands = Brand.objects.all()

        self.assertEqual(len(brands), 0)

    def test_delete_brand_fails_when_invalid_brand_id(self):
        """Test deleting a brand"""
        # Create a dummy brand
        Brand.objects.create(name='Brand Test Name', category='Test Category')

        url = unique_brand_url(2)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
