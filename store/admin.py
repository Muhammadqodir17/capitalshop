from django.contrib import admin
from .models import Product, Order, CardObj, LikedObj, Comment, Size, Color, Brand, Genre, PromoCode, PromoCodeObj

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(CardObj)
admin.site.register(LikedObj)
admin.site.register(Comment)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Genre)
admin.site.register(PromoCode)
admin.site.register(PromoCodeObj)
