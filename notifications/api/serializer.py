from rest_framework import serializers
from ..models import Notification
from services.calculate import calculate_time_difference_from_now


class NotificationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = (
            "content",
            "read",
            "image",
            "id"
        )

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        # calculating the time since the message was sent
        date = calculate_time_difference_from_now(instance.created_at)
        repr_["date_info"] = date
        return repr_


class NotificationsDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = (
            "content",
            "id"
        )


