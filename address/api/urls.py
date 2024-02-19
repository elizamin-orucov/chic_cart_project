from django.urls import path
from . import views

app_name = "address_api"

urlpatterns = [
    path("list/and/create/", views.AddressListCreateView.as_view(), name="list_and_create"),
    path("edit/", views.AddressEditView.as_view(), name="address_edit"),
]
