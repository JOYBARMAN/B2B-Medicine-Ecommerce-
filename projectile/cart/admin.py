from django.contrib import admin

from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username",)

    def user(self, obj):
        return obj.user.username

    user.short_description = "Customer"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "cart",
        "product",
        "quantity",
    )
    search_fields = ("cart__user__username",)

    def cart(self, obj):
        return obj.cart.user.username

    def product(self, obj):
        return obj.product.name

    cart.short_description = "Customer"
    product.short_description = "Product"
