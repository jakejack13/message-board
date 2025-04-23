from django.db import models


class User(models.Model):
    """A model that represents a user in the message board application"""
    username = models.CharField(max_length=100, unique=True)
    """The username of the user"""
    hashed_password = models.IntegerField()
    """The hashed and salted password of the user"""
    password_salt = models.CharField(max_length=20)


class Message(models.Model):
    """A model that represents a message in the message board
    application"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """The user that created this message"""
    message = models.CharField(max_length=500)
    """The text of the message"""

    def json(self):
        """Returns the JSON representation of this message"""
        return {'username': self.user.username, 'message': self.message}
