"""Views for Cart"""
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    CreateAPIView,
)
from rest_framework.response import Response
from rest_framework import status

from shop.permissions import IsCustomerUser
from common.renderers import ErrorRenderers
from cart.models import Cart, CartItem
from cart.rest.serializers.cart import CartSerializer, AddCartItemSerializer


class CartList(RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsCustomerUser]
    renderer_classes = [ErrorRenderers]

    def get_object(self):
        return (
            Cart()
            .get_all_actives()
            .select_related("user")
            .prefetch_related("cart_items__product")
            .get(user=self.request.user)
        )


class AddCartItem(CreateAPIView):
    serializer_class = AddCartItemSerializer
    permission_classes = [IsCustomerUser]
    renderer_classes = [ErrorRenderers]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"user": self.request.user, "uid": kwargs.get("prod_uid")},
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        return Response(response_data, status=status.HTTP_201_CREATED)


class UpdateCartItem(RetrieveUpdateAPIView):
    serializer_class = AddCartItemSerializer
    permission_classes = [IsCustomerUser]
    renderer_classes = [ErrorRenderers]
    lookup_field = "uid"
    queryset = CartItem().get_all_actives()
