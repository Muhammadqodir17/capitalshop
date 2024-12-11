from django.db import models
from config.base_models import BaseModel
from authentication.models import User


class Tag(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='posts/')
    description = models.TextField()
    view_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)

    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class BlogComment(BaseModel):
    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}'


class Contact(BaseModel):
    message = models.TextField()
    email = models.EmailField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"
