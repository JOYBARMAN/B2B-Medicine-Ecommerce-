"""Model design for shop and shop user"""
import random

from django.db import models
from django.core.exceptions import ValidationError

from common.models import BaseModelWithUID
from core.models import User


class Shop(BaseModelWithUID):
    merchant = models.ForeignKey(
        User, on_delete=models.CASCADE, db_index=True, related_name="shop_merchant"
    )
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    website = models.URLField(
        blank=True, null=True, help_text="URL of the shop's website"
    )
    established_date = models.DateField(
        blank=True, null=True, help_text="Date when the shop was established"
    )
    domain = models.CharField(
        max_length=255, blank=True, null=True, unique=True, db_index=True
    )

    def save(self, *args, **kwargs):
        # Make domain from name and remove space
        domain = self.name.lower().replace(" ", "")

        if not self.domain:
            self.domain = f"{domain}.localhost:3000.com"

            # Check domain already exits or not
            if Shop.objects.filter(domain=self.domain).exists():
                domain = domain + str(random.randint(0000, 9999))
                self.domain = f"{domain}.localhost:3000.com"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"shop : {self.name}, merchant : {self.merchant.username}"

    class Meta:
        verbose_name = "Merchant Shop"
        verbose_name_plural = "Merchant Shops"
