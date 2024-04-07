from django.db import models
from services.generator import CodeGenerator
from django.utils.encoding import smart_bytes
from django.contrib.auth import get_user_model
from services.mixin import DateMixin, SlugMixin
from django.utils.http import urlsafe_base64_encode
from services.choices import ORDER_STATUS_CHOICES, TRACK_ORDER_STATUS


User = get_user_model()


class PromoCode(DateMixin):
    promo_code = models.CharField(unique=True, max_length=50)
    discount_price = models.PositiveIntegerField()
    users = models.ManyToManyField(User, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.promo_code

    class Meta:
        verbose_name = "code"
        verbose_name_plural = "Promo Codes"


class Order(SlugMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default="Order Received")
    shipping_address_name = models.CharField(max_length=250, blank=True, null=True, default="Free")
    shipping_address = models.CharField(max_length=250, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    promo_code = models.CharField(max_length=50, blank=True, null=True)
    shipping = models.CharField(max_length=100, blank=True, null=True)
    delivery_date = models.DateField(auto_now_add=True)
    subtotal = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = CodeGenerator().create_product_shortcode(size=12, model_=self.__class__)
        if not self.slug:
            self.slug = f"{urlsafe_base64_encode(smart_bytes(self.id))}{self.code[:3]}"
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "Orders"


class OrderItem(DateMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product_name = models.CharField(max_length=250)
    quantity = models.PositiveIntegerField()
    sku = models.CharField(max_length=50)
    total_price = models.FloatField()

    def __str__(self):
        return self.order.user.email

    class Meta:
        verbose_name = "item"
        verbose_name_plural = "Items"


class OrderTrack(DateMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=70, choices=TRACK_ORDER_STATUS, default="Sender is preparing to ship your order")

    def __str__(self):
        return self.order.user.email

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "Track Order"








