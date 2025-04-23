import random

from .models import User, Message

class _UserService:
    """A service that operates on users"""
    class UserAlreadyExistsException(Exception):
        """An exception thrown if a user already exists when creating a
        new user"""
        pass

    def _get_hashed_password(self, password: str, salt: str) -> int:
        """Returns the hashed and salted password"""
        return hash(password + salt)
    
    def does_user_exist(self, username: str) -> bool:
        """Returns if a user exists with the given username"""
        return User.objects.filter(username=username).exists()
    
    def get_user(self, username: str) -> User:
        """Returns the user associated with the given username"""
        return User.objects.get(username=username)

    def create_user(self, username: str, password: str):
        """Creates a new user with the given username and password"""
        if self.does_user_exist(username):
            raise _UserService.UserAlreadyExistsException()
        salt = str(random.randbytes(20))
        hashed_password = self._get_hashed_password(password, salt)
        User.objects.create(username=username, hashed_password=hashed_password, password_salt=salt)
    
    def check_user_login(self, username: str, password: str) -> bool:
        """Returns if the a user exists with the given username and has 
        the given password"""
        if not self.does_user_exist(username):
            return False
        user = User.objects.get(username=username)
        salt = user.password_salt
        hashed_password = self._get_hashed_password(password, salt)
        return hashed_password == user.hashed_password


class _MessageService:
    """A service that operates on messages"""
    
    def get_all_messages(self) -> list[Message]:
        """Returns a list of all of the messages in the system, ordered
        by creation time"""
        return list(Message.objects.all())
    
    def get_user_messages(self, user: User) -> list[Message]:
        """Returns a list of messages sent by the given user, ordered
        by creation time"""
        return list(Message.objects.filter(user=user))
    
    def create_message(self, user: User, message: str):
        """Creates a new message on the message board from the given user"""
        Message.objects.create(user=user, message=message)


USER_SERVICE = _UserService()
"""The single instance of the user service"""
MESSAGE_SERVICE = _MessageService()
"""The single instance of the message service"""
