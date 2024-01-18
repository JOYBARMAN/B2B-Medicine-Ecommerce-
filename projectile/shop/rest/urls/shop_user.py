"""Url for shop user"""
from django.urls import path
from shop.rest.views.shop_user import ShopUserList,ShopUserDetail

urlpatterns = [
    path("/users", ShopUserList.as_view(), name="shop-user-list"),
    path("/users/<uuid:uid>", ShopUserDetail.as_view(), name="shop-user-detail"),
]