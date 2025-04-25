"""Module for registering user models with the admin page"""

from django.contrib import admin

from .models import User, Message

admin.site.register(User)
admin.site.register(Message)
