from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .fields import LowerCaseCharField, LowerCaseEmailField
from .managers import UserManager
from .validators import username_validator, email_validator
from .utils import upload_img_url


class User(AbstractBaseUser, PermissionsMixin):
    email = LowerCaseEmailField(_("Email Address"), unique=True, null=False, validators=[email_validator])
    username = LowerCaseCharField(_("username"), max_length=50, unique=True, null=False, validators=[username_validator])
    full_name = models.CharField(_("Full Name"),max_length=100, null=True)
    profile_pic = models.ImageField(default="default.png", upload_to=upload_img_url)
    joined_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_fullname(self):
        return self.full_name

class Contact(models.Model):
    user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_id} following {self.following_user_id} '




