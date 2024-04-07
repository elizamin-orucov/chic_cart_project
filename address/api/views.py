from ..models import UserAddress
from rest_framework import generics
from .serializer import AddressSerializer
from rest_framework.permissions import IsAuthenticated


class AddressCreateView(generics.CreateAPIView):
    queryset = UserAddress.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class AddressListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


class AddressEditView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressSerializer
    lookup_field = "id"

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)




