from django.db import models

from versatileimagefield.fields import VersatileImageField

from common.models import BaseModelWithUID
from core.models import User
from .choices import UserGender, BloodGroups


def default_profile_photo():
    return "images/profile/default_profile.jpg"


class Profile(BaseModelWithUID):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=UserGender.choices, null=True, blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(
        max_length=10, choices=BloodGroups.choices, null=True, blank=True
    )
    bio = models.TextField(null=True, blank=True)
    photo = VersatileImageField(
        "profile_image", upload_to="images/profile/", default=default_profile_photo
    )
    full_address = models.TextField(null=True, blank=True)
    zip_code = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.DecimalField(
        max_digits=11, decimal_places=8, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=12, decimal_places=8, null=True, blank=True
    )
    facebook_link = models.CharField(max_length=255, null=True, blank=True)
    instagram_link = models.CharField(max_length=255, null=True, blank=True)
    twitter_link = models.CharField(max_length=255, null=True, blank=True)
    linkedin_link = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name}  {self.last_name}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "Users Profile"
