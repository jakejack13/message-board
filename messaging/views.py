from django.http import HttpRequest, HttpResponse

from .services import UserService, MessageService


def ping(_: HttpRequest) -> HttpResponse:
    """GET /messaging
    Pings the server"""
    return HttpResponse("pong")

def create_user(request: HttpRequest) -> HttpResponse:
    """POST /messaging/user
    Creates a new user of the program

    Request
    -------
    {
        "username": str,
        "password": str
    }
    
    Response
    --------
    {
        "id": int
    }"""
    pass

def get_all_messages(request: HttpRequest) -> HttpResponse:
    """GET /messaging/message
    Returns all of the messages in the system
    
    Response
    --------
    {
        "messages": [
            {
                "username": str,
                "message": str
            }
        ]
    }"""
    pass

def get_my_messages(request: HttpRequest) -> HttpResponse:
    """GET /messaging/message/me
    Returns all of the messages that you have sent
    
    Response
    --------
    {
        "messages": [
            {
                "username": str,
                "message": str
            }
        ]
    }"""
    pass

def create_message(request: HttpRequest) -> HttpResponse:
    """POST /messaging/message
    Creates a new message
    
    Request
    --------
    {
        "message": str
    }"""
    pass
