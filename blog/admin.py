from django.contrib import admin
from .models import Post, Tag, BlogComment, Category

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(BlogComment)
