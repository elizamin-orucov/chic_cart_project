from ..models import PrivacyPolicy
from rest_framework import generics
from .serializer import PrivacyPolicySerializer


class PrivacyPolicyListView(generics.ListAPIView):
    queryset = PrivacyPolicy.objects.filter(still_valid=True).order_by("created_at")
    serializer_class = PrivacyPolicySerializer

