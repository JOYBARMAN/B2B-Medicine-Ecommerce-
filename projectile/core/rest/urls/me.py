from django.urls import path
from core.rest.views.me import MeDetail

urlpatterns = [
    path("", MeDetail.as_view(), name="me-details"),
]
