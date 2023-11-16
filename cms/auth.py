from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from common.models import UserToken
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions


class UserTokenAuthentication(TokenAuthentication):
    """This class is used to authenticate token."""

    model = UserToken
    keyword = 'Bearer'

    def authenticate_credentials(self, key):
        """Function to authenticate credentials."""
        model = self.get_model()
        try:
            print("key in request", key)
            token = model.objects.select_related('user').get(access_key=key)
            print("token", token)

            if token.access_key_expired < timezone.now():
                raise exceptions.AuthenticationFailed(_('Token Expired.'))

        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(
                _('User inactive or deleted.'))

        return (token.user, token)

    def authenticate_header(self, request):
        """Function to authenticate header."""
        return self.keyword
