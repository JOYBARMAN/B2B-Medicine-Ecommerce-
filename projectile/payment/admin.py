from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "payment_type",
        "total_payable",
        "is_paid",
    )
    search_fields = ("order__shop__domain",)