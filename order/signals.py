from django.db.models.signals import post_save
from .models import Order, OrderTrack
from django.dispatch import receiver


@receiver(post_save, sender=Order)
def create_order_track(sender, instance, created, **kwargs):
    if created:
        OrderTrack.objects.create(
            order=instance
        )



