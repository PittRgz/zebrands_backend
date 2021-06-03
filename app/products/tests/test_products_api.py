from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product

from products.serializers import ProductSerializer

LIST_PRODUCTS_URL = reverse('products:list')
CREATE_PRODUCT_URL = reverse('products:create')


def unique_product_url(product_id):
    """Return product Update URL"""
    return reverse('products:product', args=[product_id])


class PublicProductsAPITests(TestCase):
    """Test the publicly available Products API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_products_success(self):
        """Test that all products are retrieved for anyusers"""
        # First populate the DB with some dummy products
        Product.objects.create(sku='sku_0001', name='Test Name', price=10.0, brand='Test Brand')
        Product.objects.create(sku='sku_0002', name='Test Name 2', price=20.0, brand='Test Brand 2')

        result = self.client.get(LIST_PRODUCTS_URL)

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_create_product_fails_when_unauthorized(self):
        """Test create product when unauthorized user"""
        data = {
            'sku': 'sku_0001',
            'name': 'Test Name',
            'price': 10.0,
            'brand': 'Test Brand',
        }

        result = self.client.post(CREATE_PRODUCT_URL, data)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_product_fails_when_unauthorized(self):
        """Test edit product with PATCH when unauthorized user"""
        data = {
            'sku': 'sku_0001',
            'name': 'Test Name',
            'price': 10.0,
            'brand': 'Test Brand',
        }

        result = self.client.patch(CREATE_PRODUCT_URL, data)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_full_update_product_fails_when_unauthorized(self):
        """Test edit product with PUT when unauthorized user"""
        data = {
            'sku': 'sku_0001',
            'name': 'Test Name',
            'price': 10.0,
            'brand': 'Test Brand',
        }

        result = self.client.put(CREATE_PRODUCT_URL, data)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_product_fails_when_unauthorized(self):
        """Test edit product with PUT when unauthorized user"""
        # Create a dummy product
        product = Product.objects.create(sku='sku_0001', name='Test Name', price=10.0, brand='Test Brand')

        url = unique_product_url(product.id)
        result = self.client.delete(url)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductsAPITests(TestCase):
    """Test the private available Products API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'user@zebrands.com',
            'pass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_product_success(self):
        """Test that a product is created successfully"""
        data = {
            'sku': 'sku_0001',
            'name': 'Test Name',
            'price': 10.0,
            'brand': 'Test Brand',
        }

        self.client.post(CREATE_PRODUCT_URL, data)

        # Check if the created Product exists
        exists = Product.objects.filter(
            sku=data['sku']
        ).exists()
        self.assertTrue(exists)

    def test_create_product_fails_when_sku_already_exists(self):
        """Test that a product is not created if the SKU already exist"""
        data = {
            'sku': 'sku_0001',
            'name': 'Test Name',
            'price': 10.0,
            'brand': 'Test Brand',
        }

        # Create a product with sku = sku_0001
        Product.objects.create(sku='sku_0001', name='Test Name', price=10.0, brand='Test Brand')

        response = self.client.post(CREATE_PRODUCT_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_fails_with_unvalid_data(self):
        """Test creating a new product with invalid data"""
        data = {'sku': ''}

        result = self.client.post(CREATE_PRODUCT_URL, data)

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_parcial_update_product_success(self):
        """Test updating a product with PATCH"""
        # Create a dummy product
        product = Product.objects.create(sku='sku_0001', name='Test Name', price=10.0, brand='Test Brand')

        data = {
            'name': 'New Name',
            'brand': 'New Brand',
        }
        url = unique_product_url(product.id)
        self.client.patch(url, data)

        product.refresh_from_db()  # Refresh the product from the DB

        # Check if name and brand were successfully updated
        self.assertEqual(product.name, data['name'])
        self.assertEqual(product.brand, data['brand'])

    def test_partial_update_product_fails_when_invalid_product_id(self):
        """Test updating a product with PATCH but invalid product_id"""
        # Create a dummy product
        Product.objects.create(sku='sku_0001', name='Test Name', price=10.0, brand='Test Brand')

        data = {
            'sku': 'new_sku_0001',
            'price': 999.0,
            'brand': 'New Brand',
        }
        url = unique_product_url(2)
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_full_update_product_success(self):
        """Test updating a product with PUT"""
        # Create a dummy product
        product = Product.objects.create(sku='sku_0001', name='Test Name', price=10.0, brand='Test Brand')

        data = {
            'sku': 'new_sku_0001',
            'name': 'New Name',
            'price': 999.0,
            'brand': 'New Brand',
        }
        url = unique_product_url(product.id)
        self.client.put(url, data)

        product.refresh_from_db()  # Refresh the product from the DB

        # Check if name and brand were successfully updated
        self.assertEqual(product.sku, data['sku'])
        self.assertEqual(product.name, data['name'])
        self.assertEqual(product.price, data['price'])
        self.assertEqual(product.brand, data['brand'])

    def test_full_update_product_fails_when_missing_parameters(self):
        """Test updating a product with PUT but missing parameters"""
        # Create a dummy product
        product = Product.objects.create(sku='sku_0001', name='Test Name', price=10.0, brand='Test Brand')

        data = {
            'sku': 'new_sku_0001',
            'price': 999.0,
            'brand': 'New Brand',
        }
        url = unique_product_url(product.id)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_full_update_product_fails_when_invalid_product_id(self):
        """Test updating a product with PUT but invalid product_id"""
        # Create a dummy product
        Product.objects.create(sku='sku_0001', name='Test Name', price=10.0, brand='Test Brand')

        data = {
            'sku': 'new_sku_0001',
            'price': 999.0,
            'brand': 'New Brand',
        }
        url = unique_product_url(2)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_product_success(self):
        """Test deleting a product"""
        # Create a dummy product
        product = Product.objects.create(sku='sku_0001', name='Test Name', price=10.0, brand='Test Brand')

        url = unique_product_url(product.id)
        self.client.delete(url)

        products = Product.objects.all()

        self.assertEqual(len(products), 0)

    def test_delete_product_fails_when_invalid_product_id(self):
        """Test deleting a product"""
        # Create a dummy product
        Product.objects.create(sku='sku_0001', name='Test Name', price=10.0, brand='Test Brand')

        url = unique_product_url(2)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
