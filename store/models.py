from django.db import models
from services.slugify import slugify
from services.uploader import Uploader
from ckeditor.fields import RichTextField
from services.generator import CodeGenerator
from base.models import Category, Color, Size
from services.choices import DISCOUNT_CHOICES
from services.mixin import DateMixin, SlugMixin


class Product(SlugMixin):
    name = models.CharField(max_length=150)
    description = RichTextField()
    color = models.ManyToManyField(Color, blank=True)
    size = models.ManyToManyField(Size, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()
    discount_interest = models.IntegerField(blank=True, null=True, choices=DISCOUNT_CHOICES)

    @property
    def total_price(self):
        discount_price = self.price * (self.discount_interest or 0) / 100
        discounted_price = self.price - discount_price
        return round(float(discounted_price), 2)

    def create_unique_slug(self, slug, index=0):
        new_slug = slug
        if index:
            new_slug = f"{slug}-{index}"
        qs = self.__class__.objects.filter(slug=new_slug)
        return self.create_unique_slug(slug, index + 1) if qs.exists() else new_slug

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = CodeGenerator.create_product_shortcode(
                size=8, model_=self.__class__
            )
        if not self.slug:
            self.slug = self.create_unique_slug(slugify(title=self.name))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "Products"


class ProductImage(DateMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=Uploader.product_image_uploader)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "image"
        verbose_name_plural = "Product Images"

