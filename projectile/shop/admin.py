from django.contrib import admin
from .models import Shop


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
