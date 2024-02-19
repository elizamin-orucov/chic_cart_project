from django.contrib import admin
from .models import PrivacyPolicy


class PrivacyAdmin(admin.ModelAdmin):
    list_display = ("policy_title", "updated_at", "created_at")
    list_filter = ("updated_at", "created_at")
    search_fields = ("policy_title",)


admin.site.register(PrivacyPolicy)



