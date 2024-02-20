from ..models import Wishlist
from store.models import Product
from rest_framework import generics
from .serializer import WishListSerializer
from rest_framework.response import Response
from django.db.models.functions import Coalesce
from django.db.models import F, Avg, IntegerField
from rest_framework.permissions import IsAuthenticated
from store.api.serializer import ProductListSerializer


class WishListView(generics.ListAPIView):
    serializer_class = WishListSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        qs = Wishlist.objects.filter(user=self.request.user)
        return qs

    def get(self, request, *args, **kwargs):
        id_list = self.get_queryset().values_list("product_id")
        products = Product.objects.annotate(
            disc_interest=Coalesce("discount_interest", 0, output_field=IntegerField()),
            disc_price=F("price") * F("disc_interest") / 100,
            totalprice=F("price") - F("disc_price"),
            rating=Avg("review__rating")
        ).filter(id__in=id_list)
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
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)




