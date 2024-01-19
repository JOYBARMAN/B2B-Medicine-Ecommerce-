"""Views for shipping address"""
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from core.permissions import SAFE_METHODS
from shop.permissions import (
    IsCustomerUser,
    IsMerchantUser,
    IsMerchantShopOrReadOnly,
    IsCustomerOrMerchant,
)
from shipping_address.models import ShippingAddress
from shipping_address.rest.serializers.shipping_address import ShippingAddressSerializer
from common.renderers import ErrorRenderers


class ShippingAddressList(ListCreateAPIView):
    """Views to get or create user shipping address"""

    serializer_class = ShippingAddressSerializer
    renderer_classes = [
        ErrorRenderers,
    ]
    permission_classes = [IsCustomerUser]

    def get_queryset(self):
        return ShippingAddress().get_all_actives().filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"user": self.request.user},
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        return Response(response_data, status=status.HTTP_201_CREATED)


class ShippingAddressDetail(RetrieveUpdateAPIView):
    """Views to update and detail user shipping address"""

    serializer_class = ShippingAddressSerializer
    renderer_classes = [
        ErrorRenderers,
    ]
    permission_classes = [IsCustomerUser]
    lookup_field = "uid"
    queryset = ShippingAddress().get_all_actives()
