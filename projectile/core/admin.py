from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserOtp


class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("id", "email", "phone", "username", "is_admin","user_type")
    list_filter = ("is_admin",)
    fieldsets = (
        ("User Credential", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username", "phone", "user_type")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email", "id")
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)


# User otp model admin site
@admin.register(UserOtp)
class UserOtpAdmin(admin.ModelAdmin):
    list_display = (
        "user_name",
        "otp_type",
        "otp",
        "is_activated",
    )
    search_fields = ("user__username",)

    def user_name(self, obj):
        return obj.user.username

    user_name.short_description = "Username"  # Set a custom column header
