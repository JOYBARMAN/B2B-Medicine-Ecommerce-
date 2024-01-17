from django.urls import path
from user_profile.rest.views.profile import ProfileDetail

urlpatterns = [
    path("", ProfileDetail.as_view(), name="profile-details"),
]
