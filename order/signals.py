from django.db.models.signals import post_save
from notifications.models import Notification
from .models import Order, OrderTrack
from django.dispatch import receiver


@receiver(post_save, sender=Order)
def create_order_track(sender, instance, created, **kwargs):
    if created:
        OrderTrack.objects.create(
            order=instance
        )


@receiver(post_save, sender=Order)
def create_user_notification(sender, instance, created, **kwargs):
    if created:
        notification_content = "Your payment has been successful, congratulations."
        Notification.objects.create(
            user=instance.user,
            content=notification_content
        )
    else:
        if instance.status == "Delivered":
            notification_content = f"Your order with number {instance.code} has been delivered."
            Notification.objects.create(
                user=instance.user,
                content=notification_content
            )




