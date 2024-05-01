from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_activated = models.BooleanField(default=False)
    identification_number = models.CharField(max_length=100, unique=True)

