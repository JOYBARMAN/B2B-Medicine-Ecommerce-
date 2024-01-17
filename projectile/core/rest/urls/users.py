from django.urls import path, include
from core.rest.views.users import UserList, UserDetail

urlpatterns = [
    path("", UserList.as_view(), name="user-list-create"),
    path("/<uuid:uid>", UserDetail.as_view(), name="user-details"),
]
