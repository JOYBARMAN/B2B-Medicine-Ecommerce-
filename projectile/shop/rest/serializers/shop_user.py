"""Serializers for shop user"""
from django.db import IntegrityError

from rest_framework import serializers

from core.models import User
from shop.models import Shop, ShopUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uid",
            "username",
            "phone",
            "email",
        ]


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            "uid",
            "name",
            "domain",
        ]


class ShopUserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUser
        fields = [
            "id",
            "uid",
            "shop",
            "shop_user",
            "user_role",
            "status",
        ]
        read_only_fields = [
            "id",
            "uid",
        ]


class ShopUserListSerializer(ShopUserBaseSerializer):
    shop = ShopSerializer(read_only=True)
    shop_user = UserSerializer(read_only=True)

    class Meta(ShopUserBaseSerializer.Meta):
        fields = ShopUserBaseSerializer.Meta.fields + []
        read_only_fields = ShopUserBaseSerializer.Meta.read_only_fields + []


class ShopUserPostSerializer(ShopUserBaseSerializer):
    class Meta(ShopUserBaseSerializer.Meta):
        fields = ShopUserBaseSerializer.Meta.fields + []
        read_only_fields = ShopUserBaseSerializer.Meta.read_only_fields + ["shop"]

    def create(self, validated_data):
        try:
            validated_data["shop"] = Shop.objects.get(domain=self.context.get("domain"))
            shop_instance = ShopUser.objects.create(**validated_data)
            serialized_instance = self.__class__(
                shop_instance, context=self.context
            ).data
            return serialized_instance
        except IntegrityError:
            raise serializers.ValidationError(
                "Shop user with the same user and role already exists."
            )


class ShopUserDetailSerializer(ShopUserBaseSerializer):
    shop = ShopSerializer(read_only=True)
    shop_user = UserSerializer(read_only=True)

    class Meta(ShopUserBaseSerializer.Meta):
        fields = ShopUserBaseSerializer.Meta.fields + [
            "created_at",
            "updated_at",
        ]
        read_only_fields = ShopUserBaseSerializer.Meta.read_only_fields + [
            "created_at",
            "updated_at",
        ]


# class ShopDetailSerializer(ShopBaseSerializer):
#     merchant = MerchantSerializer(read_only=True)

#     class Meta(ShopBaseSerializer.Meta):
#         fields = ShopBaseSerializer.Meta.fields + [
#             "merchant",
#             "domain",
#             "created_at",
#             "updated_at",
#         ]
#         read_only_fields = ShopBaseSerializer.Meta.read_only_fields + [
#             "created_at",
#             "updated_at",
#         ]
