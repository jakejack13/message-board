from django.http import HttpRequest, HttpResponse, JsonResponse
import json
from typing import Any, Optional

from .services import USER_SERVICE, MESSAGE_SERVICE
from .models import User


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
    body: dict[str, str] = _get_json_data(request)
    # If we are missing username or password, return 400
    if 'username' not in body or 'password' not in body:
        return JsonResponse({"error": "Missing username or password"}, status=400)
    username = body['username']
    password = body['password']
    if USER_SERVICE.does_user_exist(username): # If user with username already exists
        if USER_SERVICE.check_user_login(username, password): # And password is correct
            return HttpResponse(status=201) # We good!
        else: # And password is not correct
            return JsonResponse({"error": "Username has already been taken"}, status=409) # Not good :(
    USER_SERVICE.create_user(username, password) # If user does not exist, create new user
    return HttpResponse(status=201)

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
    messages = MESSAGE_SERVICE.get_all_messages() # Get all messages
    return JsonResponse({"messages": [message.json() for message in messages]}) # Convert messages to JSON

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
    auth_error = _check_auth_headers(request)
    if auth_error: # If there is an error with authentication, return it immediately
        return auth_error
    user = _get_user_from_auth(request) # Query user from auth headers
    messages = MESSAGE_SERVICE.get_user_messages(user) # Get messages from user
    return JsonResponse({"messages": [message.json() for message in messages]}) # Convert messages to JSON
 

def create_message(request: HttpRequest) -> HttpResponse:
    """POST /messaging/message
    Creates a new message
    
    Request
    --------
    {
        "message": str
    }"""
    auth_error = _check_auth_headers(request)
    if auth_error: # If there is an error with authentication, return it immediately
        return auth_error
    user = _get_user_from_auth(request) # Query user from auth headers
    body: dict[str, str] = _get_json_data(request)
    # If we are missing message, return 400
    if 'message' not in body:
        return JsonResponse({"error": "Missing message"}, status=400)
    message = body['message']
    MESSAGE_SERVICE.create_message(user, message)
    return HttpResponse(status=201)

def _get_json_data(request: HttpRequest) -> Any:
    """Deserializes the request body from JSON format"""
    return json.loads(request.body.decode('utf-8'))

def _check_auth_headers(request: HttpRequest) -> Optional[HttpResponse]:
    """Checks if there exists a user with the given `Username` and `Password`
    headers. If there is not, then return an `HttpResponse` containing an
    error message and `401 Unauthorized` code"""
    username = request.META.get('HTTP_Username')
    password = request.META.get('HTTP_Password')
    if not username or not password:
        return JsonResponse({"error": "Missing username or password header"}, status=401)
    if not USER_SERVICE.check_user_login(username, password):
        return JsonResponse({"error": "Incorrect username or password"}, status=401)
    return None

def _get_user_from_auth(request: HttpRequest) -> User:
    """Returns the `User` object representing the user as defined in the 
    headers of the request"""
    username = request.META.get('HTTP_Username')
    if not username:
        raise ValueError()
    return USER_SERVICE.get_user(username)