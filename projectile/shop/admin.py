from django.contrib import admin
from .models import Shop, ShopUser


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = (
        "merchant",
        "name",
        "phone_number",
        "email",
        "domain",
    )
    search_fields = ("name", "domain")

    def merchant(self, obj):
        return obj.merchant.username

    merchant.short_description = "Merchant"  # Set a custom column header


@admin.register(ShopUser)
class ShopUserAdmin(admin.ModelAdmin):
    list_display = (
        "shop",
        "shop_user",
        "user_role",
    )
    search_fields = ("shop__domain",)

    def shop(self, obj):
        return obj.shop.domain

    def shop_user(self, obj):
        return obj.shop_user.username

    shop.short_description = "Shop Domain"
    shop_user.short_description = "Shop User"
