from django.db import models
from config.base_models import BaseModel
from store.validators import validate_uz_phone_number
from authentication.models import User
from django.utils.translation import gettext_lazy as _

CATEGORY_CHOICES = (
    (1, 'MEN'),
    (2, 'WOMEN'),
    (3, 'BABY')
)
PAYMENT_TYPES = (
    (0, '---'),
    (1, 'CASH'),
    (2, 'CARD'),
)
ORDER_STATUS = (
    (0, 'CANCELED'),
    (1, 'PENDING'),
    (2, 'IN PROCESS'),
    (3, 'DELIVERED'),
)

TAKING_TYPE = (
    (0, '---'),
    (1, 'Uzum topshirish punkti '),
    (2, 'Kuryer orqali eshikkacha')
)
PAYMENT_STATUS = (
    (0, '---'),
    (1, 'PENDING'),
    (2, 'PAYED'),
)


class Category(BaseModel):
    name = models.CharField(_('name'), max_length=120)

    def __str__(self):
        return f'{self.name}'


class Genre(BaseModel):
    name = models.CharField(_('name'), max_length=200)

    def __str__(self):
        return f'{self.name}'


class Size(BaseModel):
    name = models.CharField(_('name'), max_length=200)

    def __str__(self):
        return f'{self.name}'


class Color(BaseModel):
    name = models.CharField(_('name'), max_length=200)

    def __str__(self):
        return f'{self.name}'


class Brand(BaseModel):
    name = models.CharField(_('name'), max_length=200)

    def __str__(self):
        return f'{self.name}'


class Product(BaseModel):
    rating = models.FloatField(_('rating'), default=0)
    rating_count = models.PositiveIntegerField(_('rating_count'), default=0)
    name = models.CharField(_('name'), max_length=100)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    category = models.IntegerField(_('category'), choices=CATEGORY_CHOICES)
    image = models.ImageField(_('image'), upload_to='products/')
    description = models.TextField(_('description'), )
    product_quantity = models.PositiveIntegerField(_('product_quantity'), default=0)
    price = models.FloatField(_('price'), default=0)
    discount = models.IntegerField(_('discount'), default=0)
    price_with_discount = models.FloatField(_('price_with_discount'), default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.price_with_discount = self.price - ((self.discount / 100) * self.price)
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return f'{self.name}'

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     self.price_with_discount = self.price * (1 - self.discount / 100)
    #     return super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class PromoCode(BaseModel):
    name = models.CharField(_('name'), max_length=12)
    discount = models.PositiveIntegerField(_('discount'), default=0)

    def __str__(self):
        return f"{self.name}"


class PromoCodeObj(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    promo = models.ForeignKey(PromoCode, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class Order(BaseModel):
    import uuid
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    promo = models.ForeignKey(PromoCode, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    total_price = models.FloatField(_('total_price'), default=0)
    delivery_address = models.CharField(_('delivery_address'), max_length=200, blank=True, null=True)  # ##
    taking_type = models.IntegerField(_('taking_type'), choices=TAKING_TYPE, default=0)  # ##
    delivery_point = models.CharField(_('delivery_point'), max_length=200, blank=True, null=True)  # ##
    first_name = models.CharField(_('first_name'), max_length=100)  ##
    last_name = models.CharField(_('last_name'), max_length=100)  ##
    email = models.EmailField(_('email'), max_length=100)  ##
    phone_number = models.CharField(_('phone_number'), max_length=13, validators=[validate_uz_phone_number])  ##
    payment_type = models.IntegerField(_('payment_type'), choices=PAYMENT_TYPES, default=0)  # ##
    payment_status = models.IntegerField(_('payment_status'), choices=PAYMENT_STATUS, default=0)  #
    status = models.IntegerField(_('status'), choices=ORDER_STATUS, default=1)
    uuid = models.UUIDField(_('uuid'), default=uuid.uuid4, editable=False)
    qr_code = models.ImageField(_('qr_code'), upload_to='qr_codes/')

    def __str__(self):
        return f"{self.user}"


class CardObj(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CharField)
    name = models.CharField(_('name'), max_length=200)
    price = models.FloatField(_('price'), default=0)
    discount = models.IntegerField(_('discount'), default=0)
    price_with_discount = models.FloatField(_('price_with_discount'), default=0)
    quantity = models.PositiveIntegerField(_('quantity'), default=0)
    total_price_with_discount = models.FloatField(_('total_price_with_discount'), default=0)
    total_price_without_discount = models.FloatField(_('total_price_without_discount'), default=0)
    ordered = models.BooleanField(_('ordered'), default=False)

    def __str__(self):
        return f'{self.name}'


class LikedObj(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CharField)

    def __str__(self):
        return f'{self.product}'


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField(_('comment'), )
    rating = models.PositiveIntegerField(_('rating'), default=0)

    def __str__(self):
        return f'{self.rating}'
