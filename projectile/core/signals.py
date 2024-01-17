from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import User, UserOtp


@receiver(post_save, sender=User)
def create_user_otp(sender, instance, created, **kwargs):
    if created:
        UserOtp.objects.create(user=instance)
