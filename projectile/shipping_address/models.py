"""model design for user shipping address"""
from django.db import models

from common.models import BaseModelWithUID
from core.models import User


class ShippingAddress(BaseModelWithUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.user.username} - {self.address_line_1}, {self.city}, {self.country}"
        )

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"
