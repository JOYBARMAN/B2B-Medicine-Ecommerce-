"""Model design for payment"""
from django.db import models

from common.models import BaseModelWithUID
from order.models import ShopOrder
from .choices import PaymentType


class Payment(BaseModelWithUID):
    order = models.OneToOneField(
        ShopOrder, on_delete=models.CASCADE, related_name="payment"
    )
    payment_type = models.CharField(
        max_length=20, choices=PaymentType.choices, default=PaymentType.UNDEFINED
    )
    total_payable = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for Order {self.order.uid}"

    class Meta:
        verbose_name = "Order Payment"
        verbose_name_plural = "Order Payments"
