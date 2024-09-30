from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


NAME_MAX_LENGTH = 30


class CustomUser(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=NAME_MAX_LENGTH)
    last_name = models.CharField(_("last name"), max_length=NAME_MAX_LENGTH)

    def __str__(self):
        return self.get_full_name()
