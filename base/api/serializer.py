from rest_framework import serializers
from ..models import Category, Color, Size


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "logo"
        )

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        qs = instance.children.all()
        if qs.exists():
            repr_["children"] = CategorySerializer(qs, many=True).data
        return repr_


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = (
            "id",
            "color"
        )


class SizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Size
        fields = (
            "id",
            "size"
        )

