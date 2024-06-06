# app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('membership/', views.membership_view, name='membership'),
    path('membership/create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('membership/success/', views.membership_success, name='membership_success'),
    path('membership/cancel/', views.membership_cancel, name='membership_cancel'),
    path('membership/upgrade/', views.upgrade_membership, name='upgrade_membership'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
]
