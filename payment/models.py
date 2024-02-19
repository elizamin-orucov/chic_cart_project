from django.db import models
from order.models import Order
from services.mixin import DateMixin
from services.choices import CARD_TYPE_CHOICES
from django.contrib.auth import get_user_model

User = get_user_model()


class Payment(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=CARD_TYPE_CHOICES)
    number = models.CharField(max_length=20)
    code = models.CharField(max_length=3)
    date = models.CharField(max_length=5)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "card"
        verbose_name_plural = "Payments"



