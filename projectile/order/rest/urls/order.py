"""Url for order"""
from django.urls import path
from order.rest.views.order import OrderList, OrderUpdate

urlpatterns = [
    path("", OrderList.as_view(), name="customer-order"),
    path("/<uuid:uid>", OrderUpdate.as_view(), name="customer-order-detail"),
]
