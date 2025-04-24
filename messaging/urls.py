"""Module for registering endpoints to their corresponding views"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_docs, name="docs"),
    path("user", views.create_user, name="user"),
    path("message", views.get_all_messages, name="message"),
    path("message/me", views.get_my_messages, name="me"),
    path("message/create", views.create_message, name="create"),
    path("message/nuke", views.delete_messages, name="nuke"),
]
