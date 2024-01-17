"""Views for shop"""
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from core.permissions import SAFE_METHODS
from shop.permissions import (
    IsMerchantUser,
    IsMerchantShopOrReadOnly,
    IsCustomerOrMerchant,
)
from shop.models import Shop
from shop.rest.serializers.shop import ShopListSerializer, ShopDetailSerializer
from common.renderers import ErrorRenderers


class ShopList(ListCreateAPIView):
    """Views to get or create shop instance"""

    serializer_class = ShopListSerializer
    renderer_classes = [
        ErrorRenderers,
    ]
    queryset = Shop().get_all_actives().select_related("merchant")

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsCustomerOrMerchant()]
        else:
            return [IsMerchantUser()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"merchant": self.request.user},
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        return Response(response_data, status=status.HTTP_201_CREATED)


class ShopDetail(RetrieveUpdateAPIView):
    """View to retrieve or update a shop instance."""

    serializer_class = ShopDetailSerializer
    renderer_classes = [
        ErrorRenderers,
    ]
    queryset = ShopList().queryset
    lookup_field = "domain"

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsCustomerOrMerchant()]
        else:
            return [IsMerchantShopOrReadOnly()]
