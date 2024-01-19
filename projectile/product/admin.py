from django.contrib import admin
from .models import Product, ProductImages, ProductStock


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "shop",
        "name",
        "price",
        "selling_price",
        "discounted_price",
        "discount",
    )
    search_fields = ("shop__domain",)

    def shop(self, obj):
        return obj.shop.domain

    shop.short_description = "Shop"


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "image",
    )
    search_fields = ("product__name",)

    def product(self, obj):
        return obj.product.name

    product.short_description = "Product Name"


@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "quantity",
    )
    search_fields = ("product__name",)

    def product(self, obj):
        return obj.product.name

    product.short_description = "Product Name"
