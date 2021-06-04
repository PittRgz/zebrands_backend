from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('', views.UserViewSet.as_view(), name='list'),
    path('manage/create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('manage/<int:user_id>/', views.ManageUserView.as_view(), name='user'),
]
