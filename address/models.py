from django.db import models
from services.mixin import DateMixin
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class UserAddress(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_name = models.CharField(max_length=250)
    phone_number = PhoneNumberField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=50)
    default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.default:
            self.__class__.objects.exclude(id=self.id).update(default=False)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "address"
        verbose_name_plural = "Address"

