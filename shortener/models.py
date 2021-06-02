import enum

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser


class GENDER(enum.Enum):
    not_specified = 1
    female = 2
    male = 3


class CustomUser(AbstractUser):
    gender = models.PositiveSmallIntegerField(
        'Gender',
        choices=tuple((s.value, s.name) for s in GENDER),
        default=GENDER.not_specified.value,
        db_index=True,
    )
    birthday = models.DateTimeField(
        'Birthday',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'User: {self.username} {self.email}'


class URL(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    original_url = models.CharField(max_length=200)
    short_url = models.CharField(max_length=200, null=True, blank=True)
    owner = models.ForeignKey(
        'shortener.CustomUser', related_name='urls', on_delete=models.CASCADE
    )

    def __str__(self):
        """A string representation of the model."""
        return f'Url: {self.short_url}'


class OnlineUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='online_user', on_delete=models.CASCADE,
    )
