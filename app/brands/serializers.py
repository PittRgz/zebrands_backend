from rest_framework import serializers

from core.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for Brand Objects"""

    class Meta:
        model = Brand
        fields = ('id', 'name', 'category', )
        read_only_fields = ('id', )

    def create(self, validated_data):
        """Create a new Brand"""
        return Brand.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update a product and return it"""
        brand = super().update(instance, validated_data)
        return brand
