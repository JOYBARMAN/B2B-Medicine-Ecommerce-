"""Permission for core app """

from rest_framework.permissions import BasePermission

from common.permission_messages import non_admin_user, not_active_account


SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class AllowAny(BasePermission):
    """
    Allow access for all user
    """

    def has_permission(self, request, view):
        return True


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdminUser(IsAuthenticated):
    """
    Allows access only to authenticated and  admin users.
    """

    message = non_admin_user

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return bool(request.user.is_staff)


class IsActivatedUser(IsAuthenticated):
    """
    Allows access only to authenticated and activated by OTP users.
    """

    message = not_active_account

    def has_permission(self, request, view):
        # Not authenticated, so no access
        if not super().has_permission(request, view):
            return False

        # Check if the user is activated by OTP
        return request.user.is_activated()