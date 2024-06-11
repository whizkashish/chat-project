# chat/urls.py
from django.urls import path
from .api_views import UserCreateView, CurrentUserDetailView
from rest_framework.authtoken.views import (
    obtain_auth_token
)

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('user-details/', CurrentUserDetailView.as_view(), name='user-details'),
    path('token/', obtain_auth_token, name='token_obtain_pair')
    
]
