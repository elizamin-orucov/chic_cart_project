from django.db import models
from services.mixin import DateMixin
from services.uploader import Uploader
from colorfield.fields import ColorField
from mptt.models import MPTTModel, TreeForeignKey


class Category(DateMixin, MPTTModel):
    name = models.CharField(max_length=150)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="children")
    logo = models.ImageField(upload_to=Uploader.category_image_uploader, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "Categories"

    class MPTTMeta:
        order_insertion_by = ['name']


class Color(DateMixin):
    color = ColorField()

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = "color"
        verbose_name_plural = "Colors"


class Size(DateMixin):
    size = models.CharField(max_length=50)

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = "size"
        verbose_name_plural = "Sizes"


