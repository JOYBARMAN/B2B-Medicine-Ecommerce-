from django.contrib import admin

from .models import ShopOrder, OrderItem


@admin.register(ShopOrder)
class ShopOrderAdmin(admin.ModelAdmin):
    list_display = (
        "uid",
        "shop",
        "user",
        "order_status",
        "total_items",
        "total_price",
    )
    search_fields = ("shop__domain",)

    def user(self, obj):
        return obj.user.username

    def shop(self, obj):
        return obj.shop.domain

    user.short_description = "Customer"
    shop.short_description = "Shop"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product",
        "quantity",
    )

    def order(self, obj):
        return obj.order.id

    def product(self, obj):
        return obj.product.name

    order.short_description = "Order Id"
    product.short_description = "Product"
