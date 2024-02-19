from django.db import models
from services.mixin import DateMixin
from ckeditor.fields import RichTextField


class PrivacyPolicy(DateMixin):
    policy_title = models.CharField(max_length=100)
    policy_text = RichTextField()
    still_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.policy_title}"

    class Meta:
        verbose_name = "policy"
        verbose_name_plural = "Policies"




