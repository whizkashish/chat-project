# urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.account_view, name='account'),
    path('account/password_change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change_form.html'), name='password_change'),
    path('account/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', views.custom_logout_view, name='custom-logout'),
]