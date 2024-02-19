from django.db.models import Avg, F
from rest_framework import serializers
from ..models import Product, ProductImage
from reviews.api.serializer import ReviewSerializer
from base.api.serializer import CategorySerializer, ColorSerializer, SizeSerializer


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = (
            "image",
        )


class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    category = CategorySerializer(read_only=True)
    totalprice = serializers.FloatField(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "slug",
            "name",
            "image",
            "rating",
            "category",
            "totalprice",
            "discount_interest"
        )
        for i in fields:
            extra_kwargs = {
                i: {"read_only": True}
            }

    def get_image(self, obj):
        return ProductImageSerializer(obj.productimage_set.first()).data


class ProductDetailSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    category = CategorySerializer()
    color = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "slug",
            "name",
            "size",
            "color",
            "price",
            "images",
            "rating",
            "category",
            "description",
            "total_price",
            "discount_interest"
        )

    def get_rating(self, obj):
        rating = (obj.review_set.aggregate(rating_=Avg(F("rating")))["rating_"] or 0)
        return round(rating, 1)

    def get_images(self, obj):
        return ProductImageSerializer(obj.productimage_set.all(), many=True).data

    def get_size(self, obj):
        return SizeSerializer(obj.size.all(), many=True).data

    def get_color(self, obj):
        return ColorSerializer(obj.color.all(), many=True).data
    
    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        reviews = ReviewSerializer(instance.review_set.filter(parent__isnull=True), many=True).data
        repr_["reviews"] = reviews
        repr_["reviews count"] = instance.review_set.count()
        return repr_


