from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("messaging/", include("messaging.urls")),
    path("admin/", admin.site.urls),
]
