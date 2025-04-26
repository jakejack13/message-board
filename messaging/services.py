"""Service classes used to interact with model objects"""

import hashlib
from typing import Optional
import uuid

from .models import User, Message


class _UserService:
    """A service that operates on users"""

    class UserAlreadyExistsException(Exception):
        """An exception thrown if a user already exists when creating a
        new user"""

    def _get_hashed_password(self, password: str, salt: uuid.UUID) -> str:
        """Returns the hashed and salted password"""
        return hashlib.sha256((password + str(salt)).encode()).hexdigest()

    def does_user_exist(self, username: str) -> bool:
        """Returns if a user exists with the given username"""
        return User.objects.filter(username=username).exists()

    def get_user(self, username: str) -> User:
        """Returns the user associated with the given username"""
        return User.objects.get(username=username)

    def create_user(self, username: str, password: str) -> None:
        """Creates a new user with the given username and password"""
        if self.does_user_exist(username):
            raise _UserService.UserAlreadyExistsException()
        salt = uuid.uuid4()
        hashed_password = self._get_hashed_password(password, salt)
        User.objects.create(
            username=username, hashed_password=hashed_password, password_salt=salt
        )

    def check_user_login(self, username: str, password: str) -> bool:
        """Returns if a user exists with the given username and has
        the given password"""
        if not self.does_user_exist(username):
            return False
        user = User.objects.get(username=username)
        salt = user.password_salt
        hashed_password = self._get_hashed_password(password, salt)
        return hashed_password == user.hashed_password


class _MessageService:
    """A service that operates on messages"""

    def get_all_messages(self, limit: int, since: Optional[int]) -> list[Message]:
        """Returns a list of all of the messages in the system, ordered
        by creation time. Returns only the most recent `limit` number of
        messages. If `since` is passed in, only returns messages with `id`
        larger than `since`"""
        if since:
            objects = Message.objects.filter(id__gt=since)
        else:
            objects = Message.objects.all()
        return list(objects)[:limit]

    def get_user_messages(self, user: User) -> list[Message]:
        """Returns a list of messages sent by the given user, ordered
        by creation time"""
        return list(Message.objects.filter(user=user))

    def get_tagged_messages(self, user: User) -> list[Message]:
        """Returns a list of messages that tagged the given user's username,
        ordered by creation time"""
        tagged_string = f"@{user.username}"
        return list(Message.objects.filter(message__icontains=tagged_string))

    def create_message(self, user: User, message: str) -> None:
        """Creates a new message on the message board from the given user"""
        Message.objects.create(user=user, message=message)

    def remove_all_messages(self) -> None:
        """Removes all messages in the system"""
        Message.objects.all().delete()


USER_SERVICE = _UserService()
"""The single instance of the user service"""
MESSAGE_SERVICE = _MessageService()
"""The single instance of the message service"""
