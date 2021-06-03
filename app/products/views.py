from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Product
from products import serializers


class ProductViewSet(viewsets.ModelViewSet):
    """
    list:
        Returns all ZeBrands Products in the database, ¡No authentication needed!
    """
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()


class ProductView(generics.RetrieveAPIView):
    """
    get:
        Returns a single ZeBrands product given an ID, ¡No authentication needed!
    """
    serializer_class = serializers.ProductSerializer
    authentication_classes = (TokenAuthentication, )

    def get_object(self):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])

        # If the user is anonymous, then increment product visits
        if not self.request.user.is_authenticated:
            product.visits += 1
            product.save()

        # product = get_object_or_404(Product, id=self.kwargs['product_id'])
        return product


class CreateProductView(generics.CreateAPIView):
    """
    post:
        Creates a ZeBrands product, ¡Authentication needed!
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.ProductSerializer


class ManageProductView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns single ZeBrands product given an ID, ¡Authentication needed!

    put:
        Updates all the information of a ZeBrands product, ¡Authentication needed!

    patch:
        Partially updates the information of a ZeBrands product, ¡Authentication needed!

    delete:
        Deletes a ZeBrands product given an ID, ¡Authentication needed!
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.ProductSerializer

    def get_object(self):
        """ Retrieves and return a product, given its ID"""
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        return product

    def delete(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        product.delete()

        return HttpResponse(status=200)
