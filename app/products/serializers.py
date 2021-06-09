from rest_framework import serializers

from core.models import Product
from utils.slack_handler import create_product_update_notification


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product Objects"""
    # brand_id = serializers.IntegerField(source='brand.id')
    # brand = serializers.CharField(source='brand.name')
    # category = serializers.CharField(source='brand.category')

    class Meta:
        model = Product
        fields = ('id', 'sku', 'name', 'price', 'brand', 'visits', )
        # fields = ('id', 'sku', 'name', 'price', 'brand_id', 'brand', 'category', 'visits', )
        read_only_fields = ('id', 'visits', )

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update a product and return it"""
        product = super().update(instance, validated_data)
        # Send a slack notification each time a Product is Updated
        create_product_update_notification(product)
        return product
