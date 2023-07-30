from django.contrib.auth.models import AbstractUser
from django.db import models

from newsletters.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    phone = models.CharField(max_length=35, verbose_name='phone',
                             **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
