"""Views for order"""
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.response import Response
from rest_framework import status

from core.permissions import SAFE_METHODS
from shop.permissions import (
    IsCustomerUser,
    IsOwnShopUser,
)
from order.models import ShopOrder
from order.rest.serializers.order import ShopOrderSerializer, OrderListSerializer
from common.renderers import ErrorRenderers


class OrderList(ListCreateAPIView):
    """Views for list and create user order"""

    renderer_classes = [
        ErrorRenderers,
    ]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsOwnShopUser()]
        else:
            return [IsCustomerUser()]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrderListSerializer
        else:
            return ShopOrderSerializer

    def get_queryset(self):
        return (
            ShopOrder()
            .get_all_actives()
            .select_related("shop", "user", "shipping_address")
            .prefetch_related("order_items")
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"user": self.request.user, "domain": kwargs.get("domain")},
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        return Response(response_data, status=status.HTTP_201_CREATED)


class OrderUpdate(RetrieveUpdateAPIView):
    """Views create user order"""

    serializer_class = ShopOrderSerializer
    renderer_classes = [ErrorRenderers]
    permission_classes = [IsOwnShopUser]
    queryset = ShopOrder().get_all_actives()
    lookup_field = "uid"
