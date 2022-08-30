from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    '''manages User account creation'''

    def create_user(self, email, password, **kwargs):
        user = self.model(email=email, password=password, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email,  password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return

    def create_agency_admin(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_agency_admin = True
        user.save()
        return user
