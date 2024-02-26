from django.db import models
from services.mixin import DateMixin
from services.uploader import Uploader
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    content = models.TextField()
    read = models.BooleanField(default=False)
    image = models.ImageField(upload_to=Uploader.notification_image_uploader, editable=False)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        # adjusting the bell image in read and unread notifications
        if self.read:
            logo_path = "static/notifications/notifications-read.png"
            self.image.save("default_user_logo.jpg", open(logo_path, "rb"), save=False)
        else:
            logo_path = "static/notifications/notifications-not-read.png"
            self.image.save("default_user_logo.jpg", open(logo_path, "rb"), save=False)
        return super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "message"
        verbose_name_plural = "Notifications"

