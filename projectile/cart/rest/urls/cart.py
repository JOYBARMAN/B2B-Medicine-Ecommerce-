"""Url for cart"""
from django.urls import path
from cart.rest.views.cart import CartList, AddCartItem, UpdateCartItem

urlpatterns = [
    path("", CartList.as_view(), name="customer-cart"),
    path("/<uuid:prod_uid>", AddCartItem.as_view(), name="add-cart-item"),
    path("/cartitems/<uuid:uid>", UpdateCartItem.as_view(), name="update-cart-item"),
]
