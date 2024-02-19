from django.urls import path
from . import views


app_name = "order_api"

urlpatterns = [
    path("check/promo/code/", views.PromoCodeCheckView.as_view(), name="code_check"),
    path("track/<order_code>/", views.OrderTrackView.as_view(), name="order_track"),
    path("detail/<code>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("cancel/", views.OrderCancelView.as_view(), name="order_cancel"),
    path("create/", views.OrderCreateView.as_view(), name="order_create"),
    path("list/", views.OrderListView.as_view(), name="order_list"),
]
