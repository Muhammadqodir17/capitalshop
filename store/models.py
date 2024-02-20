from django.db import models
from config.base_models import BaseModel


class ProductCategory(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(BaseModel):
    price = models.FloatField()
    discount = models.IntegerField(default=0)
    price_with_discount = models.FloatField(default=0)

    def calculate_discount(self):
        pass




