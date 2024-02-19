from ..models import Notification
from rest_framework import generics
from rest_framework.response import Response
from .permission import NotificationPermission
from rest_framework.permissions import IsAuthenticated
from .serializer import NotificationsSerializer, NotificationsDetailSerializer


class NotificationListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationsSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")


class NotificationDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, NotificationPermission)
    serializer_class = NotificationsDetailSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(obj).data
        # set the read mode of the notification to true
        obj.read = True
        # let's save our change
        obj.save()
        return Response(serializer)


class NotificationDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, NotificationPermission)
    serializer_class = NotificationsDetailSerializer
    lookup_field = "id"








