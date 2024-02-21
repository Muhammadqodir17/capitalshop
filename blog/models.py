from django.db import models
from ckeditor.fields import RichTextField
from config.base_models import BaseModel


class Tag(BaseModel):
    name = models.CharField(max_length=60)
    
    def __str__(self):
        return self.name


class Post(BaseModel):
    objects = None
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to='posts/')
    tag = models.ManyToManyField(Tag)
    description = RichTextField()

    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


