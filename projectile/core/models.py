"""Core models for user"""
from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import (
    BaseUserManager,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.core.validators import MinValueValidator, MaxValueValidator

from core.choices import UserType, OtpType
from common.models import BaseModelWithUID


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, phone, user_type, password=None):
        """
        Creates and saves a User with the given email, username ,password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
            user_type=user_type,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email,username and password.
        """
        user = self.create_user(email, password=password, username=username, phone=None, user_type=UserType.UNDEFINED)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseModelWithUID):
    """Users model in the System"""

    username = models.CharField(max_length=20, unique=True, db_index=True)
    phone = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_admin = models.BooleanField(
        default=False,
    )
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.UNDEFINED,
    )

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    class Meta:
        verbose_name = "System User"
        verbose_name_plural = "System Users"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def is_activated(self):
        # Check user is activated by otp
        try:
            return self.userotp.is_activated
        except UserOtp.DoesNotExist:
            return False

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class UserOtp(BaseModelWithUID):
    """Otp model for user otp verifations"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    otp_type = models.CharField(
        max_length=20,
        choices=OtpType.choices,
        default=OtpType.UNDEFINED,
    )
    otp = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(100000), MaxValueValidator(999999)],
    )
    is_activated = models.BooleanField(default=False)

    def __str__(self):
        return f"user : {self.user.username} , otp : {self.otp}, activated : {self.is_activated}"

    def is_expired(self):
        # Calculate the expiration time (5 minutes from the last update)
        expiration_time = self.updated_at + timezone.timedelta(minutes=5)

        # Compare the current time with the calculated expiration time
        current_time = timezone.now()
        return current_time > expiration_time

    class Meta:
        verbose_name = "User Otp"
        verbose_name_plural = "Users Otp"
