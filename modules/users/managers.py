# coding=utf-8

from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.utils import crypto, timezone


class UserManager(BaseUserManager):

    """User model manager."""

    def create(self, email, password, **kwargs):
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **kwargs):
        return self.create(email, password, **kwargs)

    def create_superuser(self, **kwargs):
        return self.create_user(
            is_staff=True, is_superuser=True, is_active=True, **kwargs
        )


class ConfirmationManager(models.Manager):

    """Confirmation model manager."""

    def create(self, user):
        from .models import Confirmation

        instance = Confirmation()
        instance.user = user
        instance.code = self.generate_code(user)
        instance.expired = timezone.now() + Confirmation.LIFETIME
        instance.save()

        return instance

    def generate_code(self, user, length=None, letters=None):
        """Generate unique code."""
        from .models import Confirmation

        length = length or Confirmation.CODE_LENGTH
        letters = letters or Confirmation.CODE_LETTERS
        code = None

        while not code or self.filter(code=code, user=user).exists():
            code = crypto.get_random_string(
                length=length, allowed_chars=letters
            )

        return code

    def active(self):
        """Active confirmations."""
        return self.filter(expired__gt=timezone.now())

    def for_user(self, user):
        """Concrete user confirmations."""
        return self.filter(user=user)
