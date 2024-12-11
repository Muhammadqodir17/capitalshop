from django.contrib import admin
from .models import User, CustomCard, UserCard

admin.site.register(User)
admin.site.register(CustomCard)
admin.site.register(UserCard)
