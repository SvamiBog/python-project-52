from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        unique=True, blank=False,
        max_length=150)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'))

    def __str__(self):
        return self.name
