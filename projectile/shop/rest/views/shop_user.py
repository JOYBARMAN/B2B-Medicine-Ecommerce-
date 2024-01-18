"""Views for shop user"""
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from core.permissions import SAFE_METHODS
from shop.permissions import (
    IsOwnShopUser,
)
from shop.models import ShopUser, Shop
from shop.rest.serializers.shop_user import (
    ShopUserListSerializer,
    ShopUserPostSerializer,
    ShopUserDetailSerializer,
)
from common.renderers import ErrorRenderers


class ShopUserList(ListCreateAPIView):
    """Views to get or create shop user instance"""

    renderer_classes = [
        ErrorRenderers,
    ]

    permission_classes = [IsOwnShopUser]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ShopUserListSerializer
        else:
            return ShopUserPostSerializer

    def get_queryset(self):
        return (
            ShopUser()
            .get_all_actives()
            .filter(shop__domain=self.kwargs.get("domain"))
            .select_related("shop", "shop_user")
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"domain": kwargs.get("domain")},
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        return Response(response_data, status=status.HTTP_201_CREATED)


class ShopUserDetail(RetrieveUpdateAPIView):
    """View for retrieving and updating a single shop user instance."""

    queryset = ShopUser().get_all_actives()
    lookup_field = "uid"
    permission_classes = [IsOwnShopUser]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ShopUserDetailSerializer
        else:
            return ShopUserPostSerializer
