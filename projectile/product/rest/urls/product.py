"""Url for shop product"""
from django.urls import path
from product.rest.views.product import (
    ProductList,
    ProductDetail,
    ProductImagesList,
    ProductStockDetail,
    ProductStockUpdate,
)

urlpatterns = [
    path("", ProductList.as_view(), name="shop-product-list"),
    path("/<uuid:uid>", ProductDetail.as_view(), name="shop-product-detail"),
    path("/<uuid:uid>/images", ProductImagesList.as_view(), name="shop-product-images"),
    path(
        "/<uuid:uid>/stocks",
        ProductStockDetail.as_view(),
        name="shop-product-stock-detail",
    ),
    path(
        "/<uuid:prod_uid>/stocks/<uuid:uid>",
        ProductStockUpdate.as_view(),
        name="shop-product-stock-update",
    )
]
