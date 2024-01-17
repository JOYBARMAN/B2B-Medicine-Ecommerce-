"""Permission for shop app """

from rest_framework.permissions import BasePermission

from common.permission_messages import (
    non_merchant_user,
    non_customer_user,
    non_merchant_shop,
    non_customer_or_merchant,
)
from core.permissions import IsAuthenticated
from core.choices import UserType


SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsMerchantUser(IsAuthenticated):
    """
    Allows access only to authenticated and  merchant users.
    """

    message = non_merchant_user

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return bool(request.user.user_type == UserType.MERCHANT)


class IsCustomerUser(IsAuthenticated):
    """
    Allows access only to authenticated and  customer users.
    """

    message = non_customer_user

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return bool(request.user.user_type == UserType.CUSTOMER)


class IsCustomerOrMerchant(IsAuthenticated):
    """
    Allows access only to authenticated customer and marchent .
    """

    message = non_customer_or_merchant

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return bool(request.user.user_type in [UserType.CUSTOMER, UserType.MERCHANT])


class IsMerchantShopOrReadOnly(BasePermission):
    """
    Allow access only own merchant shop
    """

    message = non_merchant_shop

    def has_object_permission(self, request, view, obj):
        # Allow access for safe methods (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # Deny access if the user is not merchant of this shop
        return obj.merchant == request.user
