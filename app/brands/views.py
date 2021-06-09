from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Brand
from brands import serializers


class BrandViewSet(viewsets.ModelViewSet):
    """
    list:
        Returns all ZeBrands brands in the database, ¡Authentication needed!
    """
    serializer_class = serializers.BrandSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Brand.objects.all()


class CreateBrandView(generics.CreateAPIView):
    """
    post:
        Creates a ZeBrands brand, ¡Authentication needed!
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.BrandSerializer


class ManageBrandView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns single ZeBrands brand given an ID, ¡Authentication needed!

    put:
        Updates all the information of a ZeBrands brand, ¡Authentication needed!

    patch:
        Partially updates the information of a ZeBrands brand, ¡Authentication needed!

    delete:
        Deletes a ZeBrands brand given an ID, ¡Authentication needed!
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.BrandSerializer

    def get_object(self):
        """ Retrieves and return a ZeBrands brand, given its ID"""
        brand = get_object_or_404(Brand, id=self.kwargs['brand_id'])
        return brand

    def delete(self, request, *args, **kwargs):
        brand = get_object_or_404(Brand, id=self.kwargs['brand_id'])
        brand.delete()

        return HttpResponse(status=200)
