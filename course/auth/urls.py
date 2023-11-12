# В файле urls.py вашего приложения
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserListView, UserDetailView, UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    # Добавьте другие URL-маршруты, если необходимо
]
