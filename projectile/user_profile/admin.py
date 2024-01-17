from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user_name",
        "full_name",
        "user_email",
        "user_phone",
        "gender",
        "blood_group",
    )
    search_fields = ("user__username",)

    def user_name(self, obj):
        return obj.user.username

    user_name.short_description = "Username"  # Set a custom column header

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Email"  # Set a custom column header

    def user_phone(self, obj):
        return (
            obj.user.phone
        )

    user_phone.short_description = "Phone"  # Set a custom column header
