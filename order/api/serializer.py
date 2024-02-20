from datetime import timedelta
from basket.models import Basket
from store.models import Product
from shipping.models import Shipping
from rest_framework import serializers
from django.db.models import FloatField, F, Sum
from django.db.models.functions import Coalesce
from store.api.serializer import ProductImageSerializer
from ..models import PromoCode, Order, OrderItem, OrderTrack


class PromoCodeSerializer(serializers.ModelSerializer):
    promo_code = serializers.CharField()

    class Meta:
        model = PromoCode
        fields = (
            "promo_code",
            "discount_price",
        )
        extra_kwargs = {
            "discount_price": {"read_only": True},
        }

    def validate(self, attrs):
        user = self.context.get("user")
        # promotional code check
        try:
            promo_code = PromoCode.objects.get(promo_code=attrs.get("promo_code"))
        except:
            raise serializers.ValidationError({"error": "Code not found."})

        # used code check
        if user in promo_code.users.all():
            raise serializers.ValidationError({"error": "You have now used this promo code."})
        # inactive code check
        if not promo_code.status:
            raise serializers.ValidationError({"error": "This promo code is no longer active."})
        return super().validate(attrs)

    def create(self, validated_data):
        return PromoCode.objects.get(promo_code=validated_data.get("promo_code"))


class OrderItemListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "image",
        )

    def get_image(self, obj):
        qs = Product.objects.filter(code=obj.sku)
        product = qs.get() if qs else None
        image = product.productimage_set.first() if product else None
        return ProductImageSerializer(image).data


class OrderItemDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = (
            "quantity",
            "total_price",
            "product_name",
        )


class OrderDetailSerializer(serializers.ModelSerializer):
    address = serializers.CharField(write_only=True)
    payment_id = serializers.CharField(write_only=True)
    shipping_id = serializers.IntegerField(write_only=True)
    tracking_number = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = (
            "total",
            "status",
            "address",
            "subtotal",
            "shipping",
            "promo_code",
            "payment_id",
            "shipping_id",
            "delivery_date",
            "payment_method",
            "tracking_number",
        )
        extra_kwargs = {
            "status": {"read_only": True},
            "subtotal": {"read_only": True},
            "delivery_date": {"read_only": True},
            "payment_method": {"read_only": True},
        }

    def validate(self, attrs):
        total = attrs.get("total")
        user = self.context.get("user")
        shipping_id = attrs.get("shipping_id")

        # card verification
        try:
            card = user.payment_set.get(id=attrs.get("payment_id"))
        except:
            raise serializers.ValidationError({"error": "Card not found."})

        # shipping method verification
        try:
            Shipping.objects.get(id=shipping_id)
        except:
            raise serializers.ValidationError({"error": "Please choose shipping time."})

        # sufficient balance check
        if card.balance < total:
            raise serializers.ValidationError({"error": "Insufficient funds."})

        return super().validate(attrs)

    def create(self, validated_data):
        user = self.context.get("user")
        promo_code = validated_data.get("promo_code")
        payment = user.payment_set.get(id=validated_data.get("payment_id"))
        address = user.useraddress_set.get(id=validated_data.get("address"))
        shipping = Shipping.objects.get(id=validated_data.get("shipping_id"))

        # calculating the total price of the products in the basket
        basket_list = Basket.objects.annotate(
            discount_interest=Coalesce(F("product__discount_interest"), 0, output_field=FloatField()),
            product_disc_prc=F("product__price") * F("discount_interest")/100,
            total_price=F("product__price") - F("product_disc_prc"),
            subtotal=F("total_price") * F("quantity")
        ).filter(user=user)

        # getting promo code discount price
        promo_code_disc = PromoCode.objects.get(promo_code=promo_code).discount_price if promo_code else 0
        # calculation of subtotal price
        subtotal = basket_list.aggregate(total=Sum("subtotal")).get("total") + shipping.price
        # create new order
        new_order = Order.objects.create(
            user=user,
            subtotal=subtotal,
            shipping=shipping.name,
            payment_method=payment.name,
            total=subtotal - promo_code_disc,
            shipping_address_name=address.address_name,
            promo_code=validated_data.get("promo_code"),
            shipping_address=f"{address.city},{address.state}",
        )
        # updating the estimated time in accordance with the selected shipping period
        new_order.delivery_date += timedelta(days=shipping.duration)
        new_order.save()

        # creation of order items
        for _ in basket_list:
            OrderItem.objects.create(
                order=new_order,
                sku=_.product.code,
                quantity=_.quantity,
                product_name=_.product.name,
                total_price=_.product.total_price
            )
        # updating users of used promo code
        qs_promo = PromoCode.objects.filter(promo_code=promo_code)
        if qs_promo.exists():
            qs_promo.get().users.add(user)
        basket_list.delete()
        return new_order

    def get_tracking_number(self, obj):
        return obj.code

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_["order info"] = OrderItemDetailSerializer(
            instance.order_items.all(), many=True
        ).data
        repr_["delivery location"] = {
            "address category": instance.shipping_address_name,
            "location": instance.shipping_address
        }
        return repr_


class OrderListSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = (
            "date",
            "code",
            "total",
            "status",
        )

    # change date type
    def get_date(self, obj):
        return obj.created_at.strftime("%d %B %Y")

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        qs = instance.order_items.all()
        # picture list of order items
        repr_["items_images"] = OrderItemListSerializer(qs, many=True).data
        return repr_


class OrderCancelSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Order
        fields = (
            "code",
            "status",
        )
        extra_kwargs = {
            "status": {"read_only": True}
        }

    def validate(self, attrs):
        code = attrs.get("code")
        user = self.context.get("user")

        try:
            # order existence check
            order = Order.objects.get(code=code)
        except:
            raise serializers.ValidationError({"error": "Order not found."})

        # Only orders with order received status can be cancelled.
        if not order.status == "Order Received":
            raise serializers.ValidationError({"error": f"An order with status {order.status} cannot be cancelled."})

        # user control
        if not order.user == user:
            raise serializers.ValidationError({"error": "Order user is not correct."})

        return super().validate(attrs)

    def create(self, validated_data):
        code = validated_data.get("code")
        order = Order.objects.get(code=code)
        # change order status
        order.status = "Cancelled"
        # deleting trackorder objects related to the canceled order
        order.ordertrack_set.delete()
        # save order status change
        order.save()
        return order


class OrderTrackSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderTrack
        fields = (
            "date",
            "status"
        )

    def get_date(self, obj):
        return obj.created_at.strftime("%d %B %H:%M")


