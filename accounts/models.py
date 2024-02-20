from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from .managers import UserManager
from ckeditor.fields import RichTextField
from services.choices import GENDER_CHOICES
from services.generator import CodeGenerator
from phonenumber_field.modelfields import PhoneNumberField


def upload_to(instance, filename):
    return f"users/{instance.email}/{filename}"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=120)
    username = models.CharField(unique=True, max_length=250)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=upload_to, blank=True, null=True)

    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, blank=True, null=True)
    mobile = PhoneNumberField(unique=True)
    birth_day = models.DateField(blank=True, null=True)
    bio = RichTextField(blank=True, null=True)

    slug = models.SlugField(unique=True)
    activation_code = models.CharField(max_length=6, blank=True, null=True, editable=False)

    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "mobile"]

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = CodeGenerator.create_slug_shortcode(size=20, model_=self.__class__)
        if not self.logo:
            # default image for users without a profile picture
            default_logo_path = "static/user/user.jpg"
            self.logo.save("default_user_logo.jpg", open(default_logo_path, "rb"), save=False)
        return super(User, self).save(*args, **kwargs)


