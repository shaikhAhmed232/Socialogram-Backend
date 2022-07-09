from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Contact
# Register your models here.

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_from = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["username", "is_active", "is_superuser", "joined_at"]
    ordering = ['-joined_at',]
    list_filter = ["joined_at",]
    search_fields = ["username", "email"]
    fieldsets = ((None, {"fields": ("username", "email", "password")}), ("Extra Fields", {"fields" : ('full_name', "profile_pic")}), ("Permissions", {"fields": ("is_active", "is_superuser", "is_staff")}))

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "full_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )

admin.site.register(User, CustomUserAdmin)

admin.site.register(Contact)

