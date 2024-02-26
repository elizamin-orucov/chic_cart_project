from ..models import Basket
from rest_framework import serializers
from store.api.serializer import ProductImageSerializer
from base.api.serializer import ColorSerializer, SizeSerializer


class BasketListSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    color_choices = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Basket
        fields = (
            "color_choices",
            "total_price",
            "quantity",
            "image",
            "name",
            "id",
        )
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def get_image(self, obj):
        return ProductImageSerializer(obj.product.productimage_set.first()).data

    def get_name(self, obj):
        return obj.product.name

    def get_color_choices(self, obj):
        return ColorSerializer(obj.product.color.all(), many=True).data

    def get_total_price(self, obj):
        discount_price = obj.product.price * (obj.product.discount_interest or 0) / 100
        total_price = obj.product.price - discount_price
        return total_price

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_["product_color"] = ColorSerializer(instance.color).data
        if instance.product.size.all():
            repr_["product_size"] = SizeSerializer(instance.size).data
            repr_["size_choices"] = SizeSerializer(instance.product.size.all(), many=True).data
        return repr_


class BasketCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basket
        fields = (
            "quantity",
            "product",
            "color",
            "size",

        )
        extra_kwargs = {
            "color": {"required": True},
        }


