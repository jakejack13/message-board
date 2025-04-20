from django.http import HttpRequest, HttpResponse


def ping(_: HttpRequest):
    return HttpResponse("pong")
