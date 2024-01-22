from django.db.models import TextChoices


class PaymentType(TextChoices):
    UNDEFINED = "UNDEFINED", "Undefined"
    CASH_ON_DELIVERY = "CASH_ON_DELIVERY", "Cash_On_Delivery"
    ONLINE_PAYMENT = "ONLINE_PAYMENT", "Online_Payment"
