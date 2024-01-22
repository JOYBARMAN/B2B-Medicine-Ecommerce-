"""Url for shop dashboard"""
from django.urls import path
from shop.rest.views.dashboard import ShopDashboardView

urlpatterns = [
    path("", ShopDashboardView.as_view(), name="shop-dashboard"),
]