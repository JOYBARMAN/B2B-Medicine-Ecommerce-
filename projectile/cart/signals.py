from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import User
from core.choices import UserType
from .models import Cart


@receiver(post_save, sender=User)
def create_customer_cart(sender, instance, created, **kwargs):
    if created and instance.user_type == UserType.CUSTOMER:
        Cart.objects.create(user=instance)
