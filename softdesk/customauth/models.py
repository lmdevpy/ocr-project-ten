from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class User(AbstractUser, PermissionsMixin):
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    age = models.IntegerField(blank=False)
    username = models.CharField(max_length=150, unique=True, primary_key=True)
    email = models.EmailField(max_length=254, blank=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "age"]
