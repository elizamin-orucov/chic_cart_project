from ..models import UserAddress
from rest_framework import generics
from .serializer import AddressSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class AddressListCreateView(generics.ListCreateAPIView):
    queryset = UserAddress.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressSerializer

    def get(self, request, *args, **kwargs):
        qs = self.queryset.filter(user=self.request.user)
        serializer = self.serializer_class(qs, many=True).data
        return Response(serializer)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class AddressEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    lookup_field = "id"

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)




