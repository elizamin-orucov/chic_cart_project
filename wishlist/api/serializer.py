from rest_framework import serializers
from ..models import Wishlist


class WishListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wishlist
        fields = ("product",)





