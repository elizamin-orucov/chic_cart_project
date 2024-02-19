from .serializer import (
    PromoCodeSerializer, OrderDetailSerializer, OrderListSerializer, OrderCancelSerializer,
    OrderTrackSerializer
)
from rest_framework.permissions import IsAuthenticated
from ..models import PromoCode, Order, OrderTrack
from rest_framework.response import Response
from rest_framework import generics


class PromoCodeCheckView(generics.CreateAPIView):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "code"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCancelView(generics.CreateAPIView):
    serializer_class = OrderCancelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OrderTrackView(generics.ListAPIView):
    serializer_class = OrderTrackSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        code = self.kwargs.get("order_code")
        return OrderTrack.objects.filter(
            order__user=self.request.user, order__code=code
        ).order_by("-created_at")



