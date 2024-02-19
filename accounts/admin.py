from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm

# Register your models here.

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = (
        "email",
        "username",
        "is_active",
        "is_superuser",
        "activation_code",
        "slug",
    )
    list_filter = ("is_active", "is_superuser")
    fieldsets = (
        (
            "User information",
            {
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password",
                    "logo",
                    "activation_code"
                )
            },
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (
            "Create new user",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    readonly_fields = ("timestamp",)
    search_fields = ("email", "username")
    ordering = ("email", "username")
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
