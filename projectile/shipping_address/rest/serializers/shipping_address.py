"""Serializers for shipping address"""
from rest_framework import serializers

from shipping_address.models import ShippingAddress
from core.utils import is_valid_bd_phone_num


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = [
            "id",
            "uid",
            "user",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "postal_code",
            "country",
            "phone",
            "is_default",
            "status",
        ]
        read_only_fields = [
            "id",
            "uid",
            "user",
        ]

    def validate_phone(self, value):
        if value and not is_valid_bd_phone_num(value):
            raise serializers.ValidationError(
                "This is not a valid Bangladeshi phone number "
            )
        return value

    def create(self, validated_data):
        user = self.context.get("user")
        shipping_address = ShippingAddress.objects.create(user=user, **validated_data)
        serialized_instance = self.__class__(
            shipping_address, context=self.context
        ).data
        return serialized_instance
