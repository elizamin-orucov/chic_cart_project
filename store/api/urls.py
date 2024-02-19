from django.urls import path
from . import views

app_name = "store_api"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="products_list"),
    path("discounts/", views.ProductListWithDiscountView.as_view(), name="discounts_list"),
    path("detail/<slug>/", views.ProductDetailView.as_view(), name="product_detail"),
]



