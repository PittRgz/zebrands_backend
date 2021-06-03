from django.urls import path

from products import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductViewSet.as_view({'get': 'list'}), name='list'),
    path('create/', views.CreateProductView.as_view(), name='create'),
    path('manage/<int:product_id>/', views.ManageProductView.as_view(), name='product'),
    path('<int:product_id>/', views.ProductView.as_view(), name='product_readonly'),
]
