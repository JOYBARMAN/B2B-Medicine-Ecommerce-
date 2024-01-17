"""Serializers for profile detail and update"""

from rest_framework import serializers

from core.rest.serializers.me import MeDetailSerializer
from user_profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = MeDetailSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "uid",
            "user",
            "full_name",
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "blood_group",
            "bio",
            "photo",
            "full_address",
            "zip_code",
            "latitude",
            "longitude",
            "facebook_link",
            "instagram_link",
            "twitter_link",
            "linkedin_link",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "uid",
            "created_at",
            "updated_at",
        ]
