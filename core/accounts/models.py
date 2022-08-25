from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from accounts.manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(null=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username if self.username else "user"

    class Meta:
        db_table = 'user'
