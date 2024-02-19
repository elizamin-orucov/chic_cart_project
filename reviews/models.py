from django.db import models
from store.models import Product
from services.choices import RATING
from services.mixin import DateMixin
from services.uploader import Uploader
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class Review(MPTTModel, DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, related_name="children", blank=True, null=True)
    message = models.TextField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to=Uploader.review_image_uploader, blank=True, null=True)
    rating = models.PositiveIntegerField(choices=RATING)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = "Reviews"
        verbose_name = "comment"
        ordering = ("-created_at", )



