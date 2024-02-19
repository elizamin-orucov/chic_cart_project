from django.urls import path
from . import views


app_name = "payment_api"

urlpatterns = [
    path("create/", views.CardCreateView.as_view(), name="card_create"),
    path("delete/", views.CardDeleteView.as_view(), name="card_delete"),
    path("list/", views.CardListView.as_view(), name="card_list"),
]
