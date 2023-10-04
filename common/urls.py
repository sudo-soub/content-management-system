from django.urls import path
from common import views

urlpatterns = [
    path(
        'verify-email/',
        views.VerifyEmailView.as_view(),
        name="verify-email"
    ),
    path(
        'create-account/',
        views.CreateAccount.as_view(),
        name="create-account"
    ),
    path(
        'user-login/',
        views.UserLogin.as_view(),
        name="user-login"
    ),
    path(
        'refresh-key',
        views.RefreshToken.as_view(),
        name='refresh-key'
    )
]