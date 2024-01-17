from django.db.models import TextChoices


class Status(TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    DRAFT = "DRAFT", "DRAFT"
    REMOVED = "REMOVED", "Removed"
