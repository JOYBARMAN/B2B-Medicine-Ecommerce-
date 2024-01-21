from django.db.models import TextChoices


class OrderStatus(TextChoices):
    UNDEFINED = "UNDEFINED", "Undefined"
    PENDING = "PENDING", "Pending"
    PROCESSING = "PROCESSING", "Processing"
    SHIPPED = "SHIPPED", "Shipped"
    DELIVERED = "DELIVERED", "Delivered"
    CANCELED = "CANCELED", "Canceled"
    RETURNED = "RETURNED", "Returned"
    REFUNDED = "REFUNDED", "Refunded"
