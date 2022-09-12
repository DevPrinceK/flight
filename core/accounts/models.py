from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from accounts.manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_agency_admin = models.BooleanField(default=False)
    agency = models.ForeignKey('backend.Agency', on_delete=models.CASCADE, null=True, blank=True)  # noqa
    date_joined = models.DateTimeField(auto_now_add=True)

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name if self.first_name or self.last_name else 'N/A'  # noqa

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email if self.email else "user"

    class Meta:
        db_table = 'user'
