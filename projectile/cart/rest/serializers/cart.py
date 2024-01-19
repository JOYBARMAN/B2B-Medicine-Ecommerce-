"""Serializer for cart"""
from rest_framework import serializers

from product.models import Product
from cart.models import Cart, CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "uid",
            "name",
            "selling_price",
            "discounted_price",
        ]


class CartItemSerializer(serializers.Serializer):
    uid = serializers.CharField()
    product = ProductSerializer()
    quantity = serializers.IntegerField()
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)


class CartSerializer(serializers.ModelSerializer):
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "uid",
            "user",
            "total_items",
            "total_price",
            "cart_items",
            "status",
        ]

    def get_total_items(self, obj):
        return str(obj.total_items())

    def get_total_price(self, obj):
        return str(obj.total_price())


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "id",
            "uid",
            "cart",
            "product",
            "quantity",
            "status",
        ]
        read_only_fields = [
            "id",
            "uid",
            "cart",
            "product",
        ]

    def create(self, validated_data):
        cart = Cart.objects.get(user=self.context.get("user"))
        product = Product.objects.get(uid=self.context.get("uid"))

        cart_item_instance = CartItem.objects.create(
            cart=cart, product=product, **validated_data
        )

        serialized_instance = self.__class__(
            cart_item_instance, context=self.context
        ).data
        return serialized_instance
