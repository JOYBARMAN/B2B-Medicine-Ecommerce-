"""Url for merchant shop"""
from django.urls import path
from shop.rest.views.merchant import MerchantShopList

urlpatterns = [
    path("/shops", MerchantShopList.as_view(), name="merchant-shop-list")
]