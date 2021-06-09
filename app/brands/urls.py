from django.urls import path

from brands import views

app_name = 'brands'

urlpatterns = [
    path('', views.BrandViewSet.as_view({'get': 'list'}), name='list'),
    path('create/', views.CreateBrandView.as_view(), name='create'),
    path('manage/<int:brand_id>/', views.ManageBrandView.as_view(), name='brand')
]
