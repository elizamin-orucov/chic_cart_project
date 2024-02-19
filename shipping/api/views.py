from .serializer import ShippingSerializer
from rest_framework import generics
from ..models import Shipping


class ShippingListView(generics.ListAPIView):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer


