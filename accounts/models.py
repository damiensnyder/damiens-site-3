from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    theme = models.CharField(max_length=30, default="auto")

    class Meta:
        db_table = 'auth_user'