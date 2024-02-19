from django.urls import path
from . import views

app_name = "notifications_api"

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="notifications_list"),
    path("reading/<id>/", views.NotificationDetailView.as_view(), name="notifications_detail"),
    path("delete/<id>/", views.NotificationDeleteView.as_view(), name="notifications_delete"),
]

