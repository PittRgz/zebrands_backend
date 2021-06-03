"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext as _   # For text translations
from django.views.generic import TemplateView

from rest_framework.schemas import get_schema_view

SCHEMA_TITLE = _('ZeBrands Products and Users API')
SCHEMA_DESCRIPTION = _('This is a basic API to manage ZeBrands products and users.<br><br>'
                       'First you need to create a token for authorization with your email and credentials.<br>'
                       'Then you need to add that token to the "Authorization" header of your requests in '
                       'the form: Token {valid_token}<br><br>'
                       'Notice that there are some public endpoints that do not need authentication.')

urlpatterns = [
    # Adding Schema view with rest_framework
    path('Schema/', get_schema_view(
        title=SCHEMA_TITLE,
        description=SCHEMA_DESCRIPTION
    ), name='openapi-schema'),
    # Adding API endpoints documentation with Swagger
    path('', TemplateView.as_view(
        template_name='documentation.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/users/', include('user.urls')),
    path('api/products/', include('products.urls')),
]
