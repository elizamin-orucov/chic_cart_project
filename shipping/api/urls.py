from django.urls import path
from . import views

app_name = "shipping_api"


urlpatterns = [
    path("list/", views.ShippingListView.as_view(), name="list"),
]
