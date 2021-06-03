from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework import authentication, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)  # Only authenticated users can Create new Users


class CreateTokenView(ObtainAuthToken):
    """Create a new token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# class ManageUserView(generics.RetrieveUpdateAPIView):
class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """Manage user GET, DELETE and UPDATE"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, user_id=None):
        """ Retrieve and return authenticated user"""
        user = get_object_or_404(get_user_model(), id=self.kwargs['user_id'])
        return user

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), id=self.kwargs['user_id'])
        user.delete()

        return HttpResponse(status=200)
