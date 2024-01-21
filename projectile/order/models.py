"""model design for customer cart"""
from django.db import models

from common.models import BaseModelWithUID
from core.models import User
from shop.models import Shop
from product.models import Product
from shipping_address.models import ShippingAddress
from .choices import OrderStatus


class ShopOrder(BaseModelWithUID):
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, db_index=True, related_name="shop_orders"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, db_index=True, related_name="user_orders"
    )
    order_status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    total_items = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.SET_NULL, null=True
    )

    def calculate_total_items(self):
        return sum(item.quantity for item in self.order_items.all())

    def calculate_total_price(self):
        return sum(item.subtotal() for item in self.order_items.all())

    def update_totals(self):
        self.total_items = self.calculate_total_items()
        self.total_price = self.calculate_total_price()
        self.save()

    def __str__(self):
        return f"Shop {self.shop.domain}"

    class Meta:
        verbose_name = "Shop Order"
        verbose_name_plural = "Shop Orders"


class OrderItem(BaseModelWithUID):
    order = models.ForeignKey(
        ShopOrder, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.selling_price * self.quantity

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            self.order.update_totals()
        except Exception as e:
            print(f"Error saving OrderItem: {e}")

    def __str__(self):
        return f"OrderItem {self.id} - {self.product.name}"

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
