from django.urls import path
from . import views

app_name = "reviews_api"


urlpatterns = [
    path("edit/<id>/", views.ReviewEditView.as_view(), name="review_edit"),
    path("create/", views.ReviewCreateView.as_view(), name="review_create"),
    path("delete/<id>/", views.ReviewDeleteView.as_view(), name="review_delete"),
]


