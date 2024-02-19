from django.contrib import admin
from .models import Category, Size, Color

admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Category)

