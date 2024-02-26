from rest_framework import generics
from ..models import Category, Color, Size
from .serializer import CategorySerializer, ColorSerializer, SizeSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.filter(parent__isnull=False)
    serializer_class = CategorySerializer
    lookup_field = "id"


class ColorListView(generics.ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class SizeListView(generics.ListAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

