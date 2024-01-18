from django.db.models import TextChoices


class ShopUserRole(TextChoices):
    UNDEFINED = "UNDEFINED", "Undefined"
    MERCHANT = "MERCHANT", "Merchant"
    MANAGER = "MANAGER", "Manager"
    CASHIER = "CASHIER", "Cashier"
    DELIVERER = "DELIVERER", "Deliverer"
