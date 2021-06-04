from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework import authentication, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """
    post:
        Creates a ZeBrands user in the system, ¡Authentication needed!
    """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)  # Only authenticated users can Create new Users


class CreateTokenView(ObtainAuthToken):
    """
    post:
        Creates a new Token for a ZeBrands user, ¡Authentication needed!
    """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserViewSet(generics.ListAPIView):
    """
    get:
        Returns all ZeBrands users in the database, ¡Authentication needed!
    """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = get_user_model().objects.all()



class ManageUserView(generics.RetrieveUpdateDestroyAPIView):

    """
    get:
        Returns single ZeBrands user given an ID, ¡Authentication needed!

    put:
        Updates all the information of a ZeBrands user, ¡Authentication needed!

    patch:
        Partially updates the information of a ZeBrands user, ¡Authentication needed!

    delete:
        Deletes a ZeBrands user given an ID, ¡Authentication needed!
    """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """ Retrieve and return a user, given its ID"""
        user = get_object_or_404(get_user_model(), id=self.kwargs['user_id'])
        return user

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), id=self.kwargs['user_id'])
        user.delete()

        return HttpResponse(status=200)
