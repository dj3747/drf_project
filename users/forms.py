from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "phone", "city", "avatar")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "phone", "city", "avatar", "is_active", "is_staff", "is_superuser")
