from django.db.models.signals import post_save, post_delete
from notifications.models import Notification
from django.dispatch import receiver
from .models import UserAddress


@receiver(post_save, sender=UserAddress)
def address_creation_notification(sender, instance, created, **kwargs):
    if created:
        notification_content = f"New address successfully saved."
        Notification.objects.create(
            user=instance.user,
            content=notification_content
        )


@receiver(post_delete, sender=UserAddress)
def address_deletion_notification(sender, instance, **kwargs):
    notification_content = f"Address successfully deleted."
    Notification.objects.create(
        user=instance.user,
        content=notification_content
    )

