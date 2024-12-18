from django.db import models
from django.utils.translation import gettext_lazy as _


class Contact(models.Model):
    objects = None
    message = models.TextField(_('message'))
    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email'))
    subject = models.CharField(_('subject'), max_length=120)
    is_solved = models.BooleanField(_('is_solved'), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
