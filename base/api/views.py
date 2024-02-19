from rest_framework import generics
from .serializer import CategorySerializer, ColorSerializer
from ..models import Category, Color


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ColorListView(generics.ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

