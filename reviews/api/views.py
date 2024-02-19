from ..models import Review
from rest_framework import generics
from .permissions import ReviewsPermission
from rest_framework.permissions import IsAuthenticated
from .serializer import ReviewSerializer, ReviewEditSerializer


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ReviewEditView(generics.UpdateAPIView):
    lookup_field = "id"
    serializer_class = ReviewEditSerializer
    permission_classes = (
        IsAuthenticated,
        ReviewsPermission
    )

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class ReviewDeleteView(generics.DestroyAPIView):
    lookup_field = "id"
    serializer_class = ReviewEditSerializer
    permission_classes = (
        IsAuthenticated,
        ReviewsPermission
    )

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

