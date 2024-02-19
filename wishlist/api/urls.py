from django.urls import path
from . import views

app_name = "wishlist_api"


urlpatterns = [
    path("", views.WishListView.as_view(), name="wish_list"),
    path("create/", views.WishCreateView.as_view(), name="wish_create"),
]

