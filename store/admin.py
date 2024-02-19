from django.contrib import admin
from .models import Product, ProductImage


class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "total_price", "code")
    list_filter = ("name", "created_at", "code")
    inlines = (ImageInline, )


admin.site.register(Product, ProductAdmin)

