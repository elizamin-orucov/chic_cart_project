from django.db import models
from store.models import Product
from services.mixin import DateMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class Wishlist(DateMixin):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    api = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"wish-{self.id}"

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "Wish list"



