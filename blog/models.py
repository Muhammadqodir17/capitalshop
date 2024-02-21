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
