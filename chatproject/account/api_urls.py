# chat/urls.py
from django.urls import path
from .api_views import UserCreateView, CurrentUserDetailView, UserList
from rest_framework.authtoken.views import (
    obtain_auth_token
)

urlpatterns = [
    path('register/', UserCreateView.as_view()),
    path('user-details/', CurrentUserDetailView.as_view()),
    path('user-list/', UserList.as_view()),
    path('token/', obtain_auth_token)
    
]
