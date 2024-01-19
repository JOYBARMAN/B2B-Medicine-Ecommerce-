"""Model design for shop product"""
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from common.models import BaseModelWithUID
from shop.models import Shop

from versatileimagefield.fields import VersatileImageField


class Product(BaseModelWithUID):
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, db_index=True, related_name="shop_product"
    )
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    def calculate_discounted_price(self):
        if self.selling_price and self.discount != 0.00:
            discount_amount = (self.discount / 100) * self.selling_price
            self.discounted_price = self.selling_price - discount_amount

    def save(self, *args, **kwargs):
        self.calculate_discounted_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"shop : {self.shop.domain}, product name : {self.name}"

    class Meta:
        verbose_name = "Shop Product"
        verbose_name_plural = "Shop Products"


class ProductImages(BaseModelWithUID):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images"
    )
    image = VersatileImageField(
        "product_image",
        upload_to="images/product/",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"{self.product.name}"


class ProductStock(BaseModelWithUID):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Product: {self.product.name}, Quantity: {self.quantity}"

    class Meta:
        verbose_name = "Product Stock"
        verbose_name_plural = "Product Stocks"


@receiver(post_save, sender=Product)
def create_product_stock(sender, instance, created, **kwargs):
    """
    Signal handler to create ProductStock when a new Product is created.
    """
    if created:
        ProductStock.objects.create(product=instance)
