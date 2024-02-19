from django.urls import path
from . import views

app_name = "privacy_api"

urlpatterns = [
    path("", views.PrivacyPolicyListView.as_view(), name="privacy_list"),
]

