from rest_framework import serializers
from ..models import UserAddress


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAddress
        fields = (
            "address_name",
            "phone_number",
            "city",
            "state",
            "zip_code",
            "default",
        )


