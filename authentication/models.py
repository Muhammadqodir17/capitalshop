from django.contrib.auth.models import AbstractUser
from django.db import models
from .utils import phone_validation


class User(AbstractUser):
    phone_number = models.CharField(max_length=13, validators=[phone_validation], null=True, blank=True, unique=True)
    email = models.EmailField(unique=True, blank=True)

    def __str__(self):
        return f'{self.username}'


class CustomCard(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    pan = models.IntegerField(default=0)
    cvv = models.CharField(max_length=3, blank=True, null=True)
    bank_name = models.CharField(max_length=100)
    card_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13, validators=[phone_validation], null=True, blank=True)
    balance = models.PositiveIntegerField(default=0)
    created_month = models.IntegerField(default=0)
    created_year = models.IntegerField(default=0)
    expired_month = models.IntegerField(default=0)
    expired_year = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class UserCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    pan = models.IntegerField(default=0)
    cvv = models.CharField(max_length=3, blank=True, null=True)
    bank_name = models.CharField(max_length=100)
    card_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13, validators=[phone_validation], null=True, blank=True)
    balance = models.PositiveIntegerField(default=0)
    created_month = models.IntegerField(default=0)
    created_year = models.IntegerField(default=0)
    expired_month = models.IntegerField(default=0)
    expired_year = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'