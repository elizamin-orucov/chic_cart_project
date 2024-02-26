from django.urls import path
from . import views

app_name = "base_api"

urlpatterns = [
    path("category/detail/<id>/", views.CategoryDetailView.as_view(), name="category_detail"),
    path("category/list/", views.CategoryListView.as_view(), name="category_list"),
    path("color/list/", views.ColorListView.as_view(), name="color_list"),
    path("size/list/", views.SizeListView.as_view(), name="size_list"),
]
