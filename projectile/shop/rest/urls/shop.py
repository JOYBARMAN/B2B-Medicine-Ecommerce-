"""Url for shop"""
from django.urls import path
from shop.rest.views.shop import ShopList, ShopDetail

urlpatterns = [
    path("", ShopList.as_view(), name="shop-list"),
    path("/<str:domain>", ShopDetail.as_view(), name="shop-detail"),
]
