# urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.account_view, name='account'),
    path('account/password_change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change_form.html'), name='password_change'),
    path('account/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/<slug:username>/', views.profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', views.custom_logout_view, name='custom-logout'),
]