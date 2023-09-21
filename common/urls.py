from django.urls import path
from common import views

urlpatterns = [
    path(
        'create-account/',
        views.CreateAccount.as_view(),
        name="create-account"
    ),
    path(
        'refresh-key',
        views.RefreshToken.as_view(),
        name='refresh-key'
    ),
]