from ckeditor.fields import RichTextField
from django.db import models
from config.base_models import BaseModel
from store.validators import validate_uz_phone_number


CATEGORY_CHOICES = (
    (1, 'MEN'),
    (2, 'WOMEN'),
    (3, 'BABY')
)
PAYMENT_TYPES = (
    (1, 'CASH'),
    (2, 'PAYME'),
    (3, 'CLICK')
)
ORDER_STATUS = (
    (0, 'CANCELED'),
    (1, 'PENDING'),
    (2, 'IN PROCESS'),
    (3, 'DELIVERED'),
)


class Category(BaseModel):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Product(BaseModel):
    objects = None
    name = models.CharField(max_length=100)
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=1)
    image = models.ImageField(upload_to='products/')
    description = RichTextField()
    price = models.FloatField()
    discount = models.IntegerField(default=0)
    price_with_discount = models.FloatField(default=0)
    brand = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.price_with_discount = self.price * (1 - self.discount / 100)
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Order(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.FloatField(default=0)
    delivery_address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=13, validators=[validate_uz_phone_number])
    payment_type = models.IntegerField(choices=PAYMENT_TYPES,  default=1)
    payed = models.FloatField(default=0)
    status = models.IntegerField(choices=ORDER_STATUS, default=1)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.product} :: {self.quantity} :: {self.phone_number}"



