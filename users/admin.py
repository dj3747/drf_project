from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ("id", "email", "phone", "city", "is_staff", "is_superuser")
    list_display_links = ("email",)  # 👈 делаем email кликабельным
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    ordering = ("id",)
    search_fields = ("email", "phone", "city")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("phone", "city", "avatar")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "phone",
                    "city",
                    "avatar",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
    )
