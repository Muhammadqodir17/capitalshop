from django.db import models
from abc import abstractmethod


class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @abstractmethod
    def __str__(self):
        pass