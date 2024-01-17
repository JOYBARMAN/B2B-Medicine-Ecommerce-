"""Serializers for shop"""
from rest_framework import serializers

from core.models import User
from shop.models import Shop
from core.utils import is_valid_bd_phone_num


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uid",
            "username",
            "phone",
            "email",
            "user_type",
        ]


class ShopBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            "id",
            "uid",
            "name",
            "description",
            "address",
            "phone_number",
            "email",
            "website",
            "established_date",
            "status",
        ]
        read_only_fields = [
            "id",
            "uid",
        ]

    def validate_phone_number(self, value):
        if value and not is_valid_bd_phone_num(value):
            raise serializers.ValidationError(
                "This is not a valid Bangladeshi phone number "
            )
        return value


class ShopListSerializer(ShopBaseSerializer):
    merchant = MerchantSerializer(read_only=True)

    class Meta(ShopBaseSerializer.Meta):
        fields = ShopBaseSerializer.Meta.fields + [
            "merchant",
            "domain",
        ]
        read_only_fields = ShopBaseSerializer.Meta.read_only_fields + [
            "domain",
        ]

    def create(self, validated_data):
        validated_data["merchant"] = self.context.get("merchant")
        shop_instance = Shop.objects.create(**validated_data)

        # Serialize the created instance before returning it
        serialized_instance = self.__class__(shop_instance, context=self.context).data
        return serialized_instance


class ShopDetailSerializer(ShopBaseSerializer):
    merchant = MerchantSerializer(read_only=True)

    class Meta(ShopBaseSerializer.Meta):
        fields = ShopBaseSerializer.Meta.fields + [
            "merchant",
            "domain",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ShopBaseSerializer.Meta.read_only_fields + [
            "created_at",
            "updated_at",
        ]