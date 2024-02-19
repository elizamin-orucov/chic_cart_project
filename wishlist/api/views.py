from ..models import Wishlist
from rest_framework import generics
from .serializer import WishListSerializer
from store.models import Product
from store.api.serializer import ProductListSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class WishListView(generics.ListAPIView):
    serializer_class = WishListSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        qs = Wishlist.objects.filter(user=self.request.user)
        return qs

    def get(self, request, *args, **kwargs):
        id_list = self.get_queryset().values_list("product_id")
        products = Product.objects.filter(id__in=id_list)
        serializer = ProductListSerializer(products, many=True).data
        return Response(serializer)


class WishCreateView(generics.CreateAPIView):
    queryset = Wishlist.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = WishListSerializer

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=request.data.get("product"))
        obj, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        if not created:
            obj.delete()
        return Response({"created": created})

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)




