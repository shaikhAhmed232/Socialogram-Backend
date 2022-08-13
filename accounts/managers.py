from multiprocessing.sharedctypes import Value
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

# Manger for creating user when .save() or .create() called.
class UserManager(BaseUserManager):
    def __create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError(_("username is required"))

        if not email:
            raise ValueError(_("email is required"))

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **extra_fields,
        )

        user.set_password(password)
        user.save()

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        return self.__create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.__create_user(username, email, password, **extra_fields)
        
