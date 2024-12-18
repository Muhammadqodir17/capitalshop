from django.contrib.auth.models import AbstractUser
from django.db import models
from .utils import phone_validation
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    phone_number = models.CharField(_('phone_number'), max_length=13, validators=[phone_validation])
    email = models.EmailField(_('email'), unique=True, blank=True, null=True)

    def __str__(self):
        return f'{self.username}'


class CustomCard(models.Model):
    first_name = models.CharField(_('first_name'), max_length=100)
    last_name = models.CharField(_('last_name'), max_length=100)
    pan = models.IntegerField(_('pan'), default=0)
    cvv = models.CharField(_('cvv'), max_length=3)
    bank_name = models.CharField(_('bank_name'), max_length=100)
    card_name = models.CharField(_('card_name'), max_length=100)
    phone_number = models.CharField(_('phone_number'), max_length=13, validators=[phone_validation])
    balance = models.PositiveIntegerField(_('balance'), default=0)
    created_month = models.IntegerField(_('created_month'), default=0)
    created_year = models.IntegerField(_('created_year'), default=0)
    expired_month = models.IntegerField(_('expired_month'), default=0)
    expired_year = models.IntegerField(_('expired_year'), default=0)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class UserCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(_('first_name'), max_length=100)
    last_name = models.CharField(_('last_name'), max_length=100)
    pan = models.IntegerField(_('pan'), default=0)
    cvv = models.CharField(_('cvv'), max_length=3)
    bank_name = models.CharField(_('bank_name'), max_length=100)
    card_name = models.CharField(_('card_name'), max_length=100)
    phone_number = models.CharField(_('phone_number'), max_length=13, validators=[phone_validation])
    balance = models.PositiveIntegerField(_('balance'), default=0)
    created_month = models.IntegerField(_('created_month'), default=0)
    created_year = models.IntegerField(_('created_year'), default=0)
    expired_month = models.IntegerField(_('expired_month'), default=0)
    expired_year = models.IntegerField(_('expired_year'), default=0)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'