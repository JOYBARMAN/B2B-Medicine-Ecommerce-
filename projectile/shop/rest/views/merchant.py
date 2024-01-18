"""Views for  merchant shop"""
from rest_framework.generics import ListAPIView

from shop.permissions import (
    IsMerchantUser,
)
from shop.models import Shop
from shop.rest.serializers.shop import ShopListSerializer
from common.renderers import ErrorRenderers


class MerchantShopList(ListAPIView):
    """Views to get merchant shop instance"""

    serializer_class = ShopListSerializer
    permission_classes = [IsMerchantUser]
    renderer_classes = [
        ErrorRenderers,
    ]
    queryset = Shop().get_all_actives().select_related("merchant")

    def get_queryset(self):
        return (
            Shop()
            .get_all_actives()
            .select_related("merchant")
            .filter(merchant=self.request.user)
        )
