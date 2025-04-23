"""Module for registering endpoints to their corresponding views"""
from django.urls import path

from . import views

urlpatterns = [
    path("user", views.create_user, name="user"),
    path("message", views.get_all_messages, name="message"),
    path("message/me", views.get_my_messages, name="me"),
    path("message/create", views.create_message, name="create"),
]
