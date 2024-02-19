from rest_framework import serializers
from ..models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            "id",
            "name",
            "code",
            "date",
            "number",
        )
        extra_kwargs = {
            "id": {"read_only": True}
        }

    def validate(self, attrs):
        number = attrs.get("number")
        code = attrs.get("code")

        if not len(number) == 16:
            raise serializers.ValidationError({"error": "please enter the 16 digit code."})
        if not len(code) == 3:
            raise serializers.ValidationError({"error": "code is wrong"})
        return attrs




