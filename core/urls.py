from drf_yasg.views import get_schema_view
from django.conf.urls.static import static
from rest_framework import permissions
from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from drf_yasg import openapi

urlpatterns = [
    path("admin/", admin.site.urls),
    path("notifications/", include("notifications.api.urls")),
    path("accounts/", include("accounts.api.urls")),
    path("favorite/", include("wishlist.api.urls")),
    path("shipping/", include("shipping.api.urls")),
    path("privacy/", include("privacy.api.urls")),
    path("address/", include("address.api.urls")),
    path("payment/", include("payment.api.urls")),
    path("review/", include("reviews.api.urls")),
    path("basket/", include("basket.api.urls")),
    path("store/", include("store.api.urls")),
    path("order/", include("order.api.urls")),
    path("base/", include("base.api.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# SWAGGER CONFIG

schema_view = get_schema_view(
    openapi.Info(
        title="Chic Cart API",
        default_version="v1",
        description="Documentation for API URLs",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
