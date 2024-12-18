from django.db import models
from config.base_models import BaseModel
from authentication.models import User
from django.utils.translation import gettext_lazy as _



class Tag(BaseModel):
    name = models.CharField(_('name'), max_length=100)

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(_('name'), max_length=100)

    def __str__(self):
        return self.name


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    image = models.ImageField(_('image'), upload_to='posts/')
    description = models.TextField(_('description'))
    view_count = models.PositiveIntegerField(_('view_count'), default=0)
    comment_count = models.PositiveIntegerField(_('comment_count'), default=0)

    is_published = models.BooleanField(_('is_published'), default=True)

    def __str__(self):
        return self.title


class BlogComment(BaseModel):
    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(_('message'))

    def __str__(self):
        return f'{self.user}'


class Contact(BaseModel):
    message = models.TextField(_('message'))
    email = models.EmailField(_('email'))
    name = models.CharField(_('name'), max_length=100)

    def __str__(self):
        return f"{self.name}"
