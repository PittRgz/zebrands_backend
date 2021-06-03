from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Product
from products import serializers


class ProductViewSet(viewsets.ModelViewSet):
    """View products in the database"""
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()


class CreateProductView(generics.CreateAPIView):
    """Create products in the database"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.ProductSerializer


class ManageProductView(generics.RetrieveUpdateDestroyAPIView):
    """Manage product GET, DELETE and UPDATE"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.ProductSerializer

    def get_object(self, user_id=None):
        """ Retrieve and return authenticated user"""
        user = get_object_or_404(Product, id=self.kwargs['product_id'])
        return user

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(Product, id=self.kwargs['product_id'])
        user.delete()

        return HttpResponse(status=200)
