from django.urls import path
from . import views

app_name = "basket_api"

urlpatterns = [
    path("list/", views.BasketListView.as_view(), name="basket_list"),
    path("create/", views.BasketCreateView.as_view(), name="basket_create"),
    path("update/<id>/", views.BasketUpdateView.as_view(), name="basket_update"),
    path("delete/<id>/", views.BasketDeleteView.as_view(), name="basket_delete"),
]

