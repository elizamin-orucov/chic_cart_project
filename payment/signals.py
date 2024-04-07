from django.db.models.signals import post_save, post_delete
from notifications.models import Notification
from django.dispatch import receiver
from .models import Payment


@receiver(post_save, sender=Payment)
def payment_creation_notification(sender, instance, created, **kwargs):
    if created:
        # create notification
        notification_content = f"New payment successfully saved."
        Notification.objects.create(
            user=instance.user,
            content=notification_content
        )


@receiver(post_delete, sender=Payment)
def payment_deletion_notification(sender, instance, created, **kwargs):
    notification_content = f"Your payment successfully deleted."
    Notification.objects.create(
        user=instance.user,
        content=notification_content
    )
