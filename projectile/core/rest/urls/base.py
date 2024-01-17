"""BASE url mappings for core app"""

from django.urls import path, include


urlpatterns = [
    path("", include("core.rest.urls.users"), name="users"),
    path("/me", include("core.rest.urls.me"), name="users"),
]
