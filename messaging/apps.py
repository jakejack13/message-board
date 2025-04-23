"""Module for Django application configuration classes"""
from django.apps import AppConfig


class MessagingConfig(AppConfig):
    """The config for the messaging app"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "messaging"
