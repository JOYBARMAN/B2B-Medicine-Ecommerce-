"""Views for product"""

from django.db.models import Prefetch

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework import status

from core.permissions import SAFE_METHODS
from shop.permissions import IsCustomerOrMerchant, IsOwnShopUser
from common.renderers import ErrorRenderers
from product.models import Product, ProductImages, ProductStock
from product.rest.serializers.product import (
    ProductListSerializer,
    ProductAddSerializer,
    ProductDetailSerializer,
    ProductImageAddSerializer,
    ProductImagesSerializer,
    ProductStockListSerializer,
)


class ProductList(ListCreateAPIView):
    """Views for get list and create product"""

    renderer_classes = [
        ErrorRenderers,
    ]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ProductListSerializer
        else:
            return ProductAddSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsCustomerOrMerchant()]
        else:
            return [IsOwnShopUser()]

    def get_queryset(self):
        return (
            Product()
            .get_all_actives()
            .filter(shop__domain=self.kwargs.get("domain"))
            .select_related("shop", "productstock")
            .prefetch_related(
                Prefetch(
                    "product_images",
                    queryset=ProductImages().get_all_actives(),
                )
            )
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"domain": kwargs.get("domain")},
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        return Response(response_data, status=status.HTTP_201_CREATED)


class ProductDetail(RetrieveUpdateAPIView):
    """Views for get and update product detail"""

    permission_classes = [IsOwnShopUser]
    renderer_classes = [
        ErrorRenderers,
    ]
    lookup_field = "uid"

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ProductDetailSerializer
        else:
            return ProductAddSerializer

    def get_object(self):
        return (
            Product()
            .get_all_actives()
            .filter(shop__domain=self.kwargs.get("domain"))
            .select_related("shop")
            .prefetch_related(
                Prefetch(
                    "product_images",
                    queryset=ProductImages().get_all_actives(),
                )
            )
            .get(uid=self.kwargs.get("uid"))
        )


class ProductImagesList(ListCreateAPIView):
    """Views for list and add images in a product"""

    permission_classes = [IsOwnShopUser]
    renderer_classes = [
        ErrorRenderers,
    ]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ProductImagesSerializer
        else:
            return ProductImageAddSerializer

    def get_queryset(self):
        return (
            ProductImages()
            .get_all_actives()
            .filter(product__uid=self.kwargs.get("uid"))
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"uid": kwargs.get("uid")}
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        return Response(response_data, status=status.HTTP_201_CREATED)


class ProductStockDetail(RetrieveAPIView):
    """views for product stock detail"""

    serializer_class = ProductStockListSerializer
    permission_classes = [IsOwnShopUser]
    renderer_classes = [
        ErrorRenderers,
    ]

    def get_object(self):
        return ProductStock().get_all_actives().get(product__uid=self.kwargs.get("uid"))


class ProductStockUpdate(UpdateAPIView):
    """views for product stock Update"""

    serializer_class = ProductStockListSerializer
    permission_classes = [IsOwnShopUser]
    renderer_classes = [
        ErrorRenderers,
    ]
    lookup_field = "uid"
    queryset = ProductStock().get_all_actives()
