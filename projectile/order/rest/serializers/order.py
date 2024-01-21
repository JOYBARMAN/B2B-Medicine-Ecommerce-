"""Serializers for shop order"""
from django.db import transaction
from django.db.models import F

from rest_framework import serializers

from order.models import ShopOrder, OrderItem
from cart.models import CartItem
from shop.models import Shop
from product.models import ProductStock
from common.choices import Status
from cart.rest.serializers.cart import ProductSerializer
from shop.rest.serializers.shop_user import UserSerializer, ShopSerializer
from shipping_address.rest.serializers.shipping_address import ShippingAddressSerializer


class ShopOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopOrder
        fields = [
            "id",
            "uid",
            "shop",
            "user",
            "order_status",
            "total_items",
            "total_price",
            "shipping_address",
            "status",
        ]
        read_only_fields = [
            "id",
            "uid",
            "shop",
            "user",
            "total_items",
            "total_price",
        ]

    def create(self, validated_data):
        user = self.context.get("user")
        shop = Shop.objects.get(domain=self.context.get("domain"))

        # Fetch related cart items
        cart_items = CartItem.objects.filter(
            cart__user=user, status=Status.ACTIVE
        ).select_related("product")

        with transaction.atomic():
            # create shop order
            shop_order = ShopOrder.objects.create(
                shop=shop, user=user, **validated_data
            )

            # Bulk create order items
            order_items_data = [
                {
                    "order": shop_order,
                    "product": cart_item.product,
                    "quantity": cart_item.quantity,
                }
                for cart_item in cart_items
            ]
            order_items = OrderItem.objects.bulk_create(
                [OrderItem(**data) for data in order_items_data]
            )

            # Update stock quantities
            for order_item in order_items:
                product_stock = ProductStock.objects.get(product=order_item.product)
                product_stock.quantity -= order_item.quantity
                product_stock.save()

            # Delete cart items instead of updating status
            cart_items.delete()

            # Update totals creation of OrderItems
            shop_order.update_totals()

        serialized_instance = self.__class__(shop_order, context=self.context).data
        return serialized_instance


class OrderItemSerializer(serializers.Serializer):
    uid = serializers.CharField()
    product = ProductSerializer()
    quantity = serializers.IntegerField()
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    shop = ShopSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)

    class Meta:
        model = ShopOrder
        fields = [
            "id",
            "uid",
            "shop",
            "user",
            "order_status",
            "total_items",
            "total_price",
            "order_items",
            "shipping_address",
            "status",
        ]
