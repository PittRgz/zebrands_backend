from rest_framework import serializers

from core.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product Objects"""

    class Meta:
        model = Product
        fields = ('id', 'sku', 'name', 'price', 'brand', 'visits')
        read_only_fields = ('id', 'visits')

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update a product and return it"""
        product = super().update(instance, validated_data)
        return product
