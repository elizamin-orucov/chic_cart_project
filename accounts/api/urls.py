from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "accounts_api"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("delete/", views.DeleteAccountView.as_view(), name="delete_account"),
    path("update/", views.UpdateUserProfileView.as_view(), name="update_profile"),
    path("activation/<uuid>/", views.ActivationView.as_view(), name="activation"),
    path("reset/password/", views.ResetPasswordView.as_view(), name="reset_password"),
    path("password/change/", views.PasswordChangeView.as_view(), name="password_change"),
    path("delete/check/<uuid>/", views.DeleteAccountCheckView.as_view(), name="delete_account_check"),
    path("reset/password/check/<uuid>/", views.ResetPasswordCheckView.as_view(), name="password_reset_check"),
    path("reset/password/complete/<uuid>/", views.ResetPasswordCompleteView.as_view(), name="reset_password_complete"),
]


