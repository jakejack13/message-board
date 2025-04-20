from django.db import models


class User(models.Model):
    """A model that represents a user in the message board application"""
    username = models.CharField(max_length=100, unique=True)
    """The username of the user"""
    password_hash = models.CharField(max_length=100)
    """The hashed and salted password of the user"""


class Message(models.Model):
    """A model that represents a message in the message board
    application"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """The user that created this message"""
    message = models.CharField(max_length=500)
    """The text of the message"""
