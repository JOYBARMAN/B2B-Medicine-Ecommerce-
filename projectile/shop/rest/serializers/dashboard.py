"""Serialier for dashboard"""
from rest_framework import serializers


class ShopDashboardSerializer(serializers.Serializer):
    total_sale = serializers.DecimalField(max_digits=10, decimal_places=2)
    todays_sale = serializers.DecimalField(max_digits=10, decimal_places=2)
    monthly_sale = serializers.DecimalField(max_digits=10, decimal_places=2)
