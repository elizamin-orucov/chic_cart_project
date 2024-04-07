from django.urls import path
from . import views

app_name = "address_api"

urlpatterns = [
    path("edit/<id>/", views.AddressEditView.as_view(), name="address_edit"),
    path("create/", views.AddressCreateView.as_view(), name="create"),
    path("list/", views.AddressListView.as_view(), name="list"),
]

