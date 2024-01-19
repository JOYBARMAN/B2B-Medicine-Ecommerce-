"""Url for merchant shipping address"""
from django.urls import path
from shipping_address.rest.views.shipping_address import (
    ShippingAddressList,
    ShippingAddressDetail,
)

urlpatterns = [
    path("", ShippingAddressList.as_view(), name="user-shipping-address"),
    path(
        "/<uuid:uid>", ShippingAddressDetail.as_view(), name="shipping-address-detail"
    ),
]
