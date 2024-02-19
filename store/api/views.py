from ..models import Product
from .filters import ProductFilter
from rest_framework import generics, filters
from rest_framework.response import Response
from django.db.models.functions import Coalesce
from services.pagination import CustomPagination
from django.db.models import Max, F, IntegerField, Avg, Q
from .serializer import ProductListSerializer, ProductDetailSerializer
from django_filters.rest_framework.backends import DjangoFilterBackend


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = CustomPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter
    )
    filterset_class = ProductFilter
    ordering_fields = ("totalprice", "created_at")

    def get_queryset(self):
        qs = Product.objects.annotate(
            disc_interest=Coalesce("discount_interest", 0, output_field=IntegerField()),
            disc_price=F("price") * F("disc_interest") / 100,
            totalprice=F("price") - F("disc_price"),
            rating=Avg("review__rating")
        ).order_by("-created_at")
        return qs


class ProductListWithDiscountView(generics.ListAPIView):
    queryset = Product.objects.filter(
        discount_interest__isnull=False
    ).order_by("-updated_at")
    serializer_class = ProductListSerializer
    pagination_class = CustomPagination


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"



