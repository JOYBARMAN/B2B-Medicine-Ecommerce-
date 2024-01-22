"""view for dashboard"""
from django.db.models import Sum
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from shop.rest.serializers.dashboard import ShopDashboardSerializer
from order.models import ShopOrder


class ShopDashboardView(APIView):
    def get(self, request, domain):
        shop_order = ShopOrder().get_all_actives()

        # Calculate total sale
        total_sale = (
            shop_order.filter(shop__domain=domain).aggregate(Sum("total_price"))[
                "total_price__sum"
            ]
            or 0.00
        )

        # Calculate today's sale
        today = timezone.now().date()
        todays_sale = (
            shop_order.filter(shop__domain=domain, created_at__date=today).aggregate(
                Sum("total_price")
            )["total_price__sum"]
            or 0.00
        )

        # Calculate monthly sale
        start_of_month = today.replace(day=1)
        monthly_sale = (
            shop_order.filter(
                shop__domain=domain, created_at__date__gte=start_of_month
            ).aggregate(Sum("total_price"))["total_price__sum"]
            or 0.00
        )

        # Serialize the data
        serializer = ShopDashboardSerializer(
            {
                "total_sale": total_sale,
                "todays_sale": todays_sale,
                "monthly_sale": monthly_sale,
            }
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
