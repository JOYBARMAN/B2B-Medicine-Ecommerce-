"""Serializers for me detail or update"""

from rest_framework import serializers

from core.models import User
from core.utils import is_valid_bd_phone_num


class MeDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, min_length=8, required=True
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, min_length=8, required=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "uid",
            "username",
            "phone",
            "email",
            "is_active",
            "is_admin",
            "user_type",
            "status",
            "password",
            "confirm_password",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "uid",
            "is_active",
            "is_admin",
            "created_at",
            "updated_at",
        ]

    def validate_phone(self, value):
        if value and not is_valid_bd_phone_num(value):
            raise serializers.ValidationError(
                "This is not a valid Bangladeshi phone number "
            )
        return value

    def validate_password(self, value):
        confirm_password = self.initial_data.get("confirm_password", "")

        if value != confirm_password:
            raise serializers.ValidationError(
                "password and confirm password do not match."
            )

        return value
