from django.contrib import admin

from .models import ShippingAddress


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "address_line_1",
        "city",
        "state",
        "country",
    )
    search_fields = ("user__username",)

    def user(self, obj):
        return obj.user.username

    user.short_description = "User"
