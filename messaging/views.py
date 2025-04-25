"""The views of the application. Each function corresponds
to a view, which is a single endpoint of the app"""

import json
import os
from typing import Any, Optional
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import markdown

from .services import USER_SERVICE, MESSAGE_SERVICE
from .models import User


def _get_docs_content() -> str:
    """Returns the docs markdown page as a single string"""
    with open("messaging/messaging.md", "r", encoding="utf-8") as f:
        content = f.read()
        return content.replace(
            "json", ""
        )  # `markdown` does not remove language indicators from code blocks


DOCS_CONTENT = _get_docs_content()

# Views


@csrf_exempt
def get_docs(request: HttpRequest) -> HttpResponse:
    """GET /messaging
    Returns the documentation for the API"""
    template = loader.get_template("messaging/docs.html")
    html = markdown.markdown(DOCS_CONTENT)
    context = {"html": html}
    return HttpResponse(template.render(context, request))


@csrf_exempt
def create_user(request: HttpRequest) -> HttpResponse:
    """POST /messaging/user
    Creates a new user of the program

    Request
    -------
    {
        "username": str,
        "password": str
    }"""
    if request.method != "POST":
        return HttpResponse(status=405)
    body: dict[str, str] = _get_json_data(request)
    # If we are missing username or password, return 400
    if "username" not in body or "password" not in body:
        return JsonResponse({"error": "Missing username or password"}, status=400)
    username = body["username"]
    password = body["password"]
    if USER_SERVICE.does_user_exist(username):  # If user with username already exists
        if USER_SERVICE.check_user_login(username, password):  # And password is correct
            return HttpResponse(status=201)  # We good!
        return JsonResponse(  # If password is not correct, we return an error
            {"error": "Username has already been taken"}, status=409
        )
    USER_SERVICE.create_user(
        username, password
    )  # If user does not exist, create new user
    return HttpResponse(status=201)


@csrf_exempt
def get_all_messages(request: HttpRequest) -> HttpResponse:
    """GET /messaging/message
    Returns all of the messages in the system

    Response
    --------
    {
        "messages": [
            {
                "id": int,
                "username": str,
                "message": str
            }
        ]
    }"""
    if request.method != "GET":
        return HttpResponse(status=405)
    try:
        limit = int(request.GET.get("limit", 100))  # Grab `limit` query param
    except ValueError:
        return JsonResponse({"error": "Invalid `limit` param"}, status=400)
    messages = MESSAGE_SERVICE.get_all_messages(limit)  # Get all messages
    return JsonResponse(
        {
            "messages": [message.json() for message in messages]
        }  # Convert messages to JSON
    )


@csrf_exempt
def get_my_messages(request: HttpRequest) -> HttpResponse:
    """GET /messaging/message/me
    Returns all of the messages that you have sent

    Response
    --------
    {
        "messages": [
            {
                "id": int,
                "username": str,
                "message": str
            }
        ]
    }"""
    if request.method != "GET":
        return HttpResponse(status=405)
    auth_error = _check_auth_headers(request)
    if auth_error:  # If there is an error with authentication, return it immediately
        return auth_error
    user = _get_user_from_auth(request)  # Query user from auth headers
    messages = MESSAGE_SERVICE.get_user_messages(user)  # Get messages from user
    return JsonResponse(
        {
            "messages": [message.json() for message in messages]
        }  # Convert messages to JSON
    )


@csrf_exempt
def get_tagged_messages(request: HttpRequest) -> HttpResponse:
    """GET /messaging/message/tagged
    Returns all of the messages that have tagged you

    Response
    --------
    {
        "messages": [
            {
                "id": int,
                "username": str,
                "message": str
            }
        ]
    }"""
    if request.method != "GET":
        return HttpResponse(status=405)
    auth_error = _check_auth_headers(request)
    if auth_error:  # If there is an error with authentication, return it immediately
        return auth_error
    user = _get_user_from_auth(request)  # Query user from auth headers
    messages = MESSAGE_SERVICE.get_tagged_messages(user)  # Get messages from user
    return JsonResponse(
        {
            "messages": [message.json() for message in messages]
        }  # Convert messages to JSON
    )


@csrf_exempt
def create_message(request: HttpRequest) -> HttpResponse:
    """POST /messaging/message/create
    Creates a new message

    Request
    --------
    {
        "message": str
    }"""
    if request.method != "POST":
        return HttpResponse(status=405)
    auth_error = _check_auth_headers(request)
    if auth_error:  # If there is an error with authentication, return it immediately
        return auth_error
    user = _get_user_from_auth(request)  # Query user from auth headers
    body: dict[str, str] = _get_json_data(request)
    # If we are missing message, return 400
    if "message" not in body:
        return JsonResponse({"error": "Missing message"}, status=400)
    message = body["message"]
    MESSAGE_SERVICE.create_message(user, message)
    return HttpResponse(status=201)


@csrf_exempt
def delete_messages(request: HttpRequest) -> HttpResponse:
    """DELETE /messaging/message/nuke
    Deletes all messages in the system"""
    if request.method != "DELETE":
        return HttpResponse(status=405)
    auth_error = _check_auth_headers(request)
    if auth_error:  # If there is an error with authentication, return it immediately
        return auth_error
    user = _get_user_from_auth(request)  # Query user from auth headers
    correct_username = os.environ["SUPERUSER"]
    if user.username != correct_username:
        return HttpResponse(status=403)
    MESSAGE_SERVICE.remove_all_messages()
    return HttpResponse(status=200)


# Helpers


def _get_json_data(request: HttpRequest) -> Any:
    """Deserializes the request body from JSON format"""
    return json.loads(request.body.decode("utf-8"))


def _check_auth_headers(request: HttpRequest) -> Optional[HttpResponse]:
    """Checks if there exists a user with the given `Username` and `Password`
    headers. If there is not, then return an `HttpResponse` containing an
    error message and `401 Unauthorized` code"""
    username = request.META.get("HTTP_USERNAME")
    password = request.META.get("HTTP_PASSWORD")
    if not username or not password:
        return JsonResponse(
            {"error": "Missing username or password header"}, status=401
        )
    if not USER_SERVICE.check_user_login(username, password):
        return JsonResponse({"error": "Incorrect username or password"}, status=401)
    return None


def _get_user_from_auth(request: HttpRequest) -> User:
    """Returns the `User` object representing the user as defined in the
    headers of the request"""
    username = request.META.get("HTTP_USERNAME")
    if not username:
        raise ValueError()
    return USER_SERVICE.get_user(username)
