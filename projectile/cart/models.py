"""model design for customer cart"""
from django.db import models

from common.models import BaseModelWithUID
from core.models import User
from product.models import Product


class Cart(BaseModelWithUID):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def total_items(self):
        return sum(item.quantity for item in self.cart_items.all())

    def total_price(self):
        return sum(item.subtotal() for item in self.cart_items.all())

    def __str__(self):
        return f"user : {self.user.username}"

    class Meta:
        verbose_name = "Customer Cart"
        verbose_name_plural = "Customer Carts"


class CartItem(BaseModelWithUID):
    cart = models.ForeignKey(
        Cart, related_name="cart_items", on_delete=models.CASCADE, db_index=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.selling_price * self.quantity

    def __str__(self):
        return f"cart : {self.cart}"

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
