# coding=utf-8

import string

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from . import managers


class User(AbstractBaseUser):

    """User database model."""

    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(_('Name'), max_length=35)
    surname = models.CharField(_('Surname'), max_length=35)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = managers.UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    def __unicode__(self):
        return u'{}'.format(self.email)

    def get_short_name(self):
        return u'{}'.format(self.name)

    def get_full_name(self):
        return u'{0.name} {0.surname}'.format(self)

    def has_module_perms(self, *args, **kwargs):
        return self.is_staff

    def has_perm(self, *args, **kwargs):
        return self.is_staff


class Confirmation(models.Model):

    """Confirmation database model."""

    LIFETIME = timezone.timedelta(days=7)
    CODE_LENGTH = 6
    CODE_LETTERS = string.digits

    user = models.ForeignKey(User, related_name='confirmations')
    code = models.CharField(max_length=32, unique=True)
    expired = models.DateTimeField()

    objects = managers.ConfirmationManager()

    class Meta:
        unique_together = ('user', 'code')
