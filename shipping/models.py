from django.db import models
from services.mixin import DateMixin


class Shipping(DateMixin):
    name = models.CharField(max_length=100)
    duration = models.IntegerField(default=1)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "method"
        verbose_name_plural = "Shipping methods"

