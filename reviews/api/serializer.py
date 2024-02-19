from rest_framework import serializers
from ..models import Review
from accounts.api.serializer import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    userinfo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields = (
            "id",
            "userinfo",
            "rating",
            "parent",
            "message",
            "product",
            "image"
        )
        extra_kwargs = {
            "product": {"write_only": True},
            "parent": {"write_only": True},
            "id": {"read_only": True},
        }

    def get_userinfo(self, obj):
        info = UserSerializer(obj.user).data
        return info

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        qs = instance.children.all()
        if qs.exists():
            repr_["replies"] = ReviewSerializer(qs, many=True).data
        return repr_


class ReviewEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = (
            "rating",
            "image",
            "message",
        )








