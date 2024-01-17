from django.db.models import TextChoices


class UserType(TextChoices):
    UNDEFINED = "UNDEFINED", "Undefined"
    MERCHANT = "MERCHANT", "Merchant"
    CUSTOMER = "CUSTOMER", "Customer"


class OtpType(TextChoices):
    REGISTRATION = "REGISTRATION", "Registration"
    LOGIN = "LOGIN", "Login"
    UNDEFINED = "UNDEFINED", "Undefined"
