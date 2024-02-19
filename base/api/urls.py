from django.urls import path
from . import views

app_name = "base_api"

urlpatterns = [
    path("category/list/", views.CategoryListView.as_view(), name="category_list"),
    path("color/list/", views.ColorListView.as_view(), name="color_list"),
]
