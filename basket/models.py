from django.db import models
from services.mixin import DateMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class Basket(DateMixin):
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE)
    api = models.CharField(max_length=150, blank=True, null=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey("base.Size", on_delete=models.SET_NULL, blank=True, null=True)
    color = models.ForeignKey("base.Color", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "Basket"

