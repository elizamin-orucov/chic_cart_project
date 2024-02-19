from rest_framework import serializers
from ..models import PrivacyPolicy


class PrivacyPolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = PrivacyPolicy
        fields = (
            "policy_title",
            "policy_text"
        )
