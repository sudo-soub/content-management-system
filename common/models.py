import datetime
import os
import binascii

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


class UserToken(models.Model):
    """The default authorization token model."""

    user = models.ForeignKey(
        User,
        related_name='user_auth_token',
        on_delete=models.CASCADE,
        verbose_name=("User")
    )
    access_key = models.CharField(("Key"), max_length=40, primary_key=True)
    refresh_key = models.CharField(
        ("refresh_key"), max_length=40, default="", null=True, blank=True)
    created = models.DateTimeField(("Created"))
    access_key_expired = models.DateTimeField(("Expired"))
    refresh_key_expired = models.DateTimeField(
        ("Refresh Key Expired"), null=True, blank=True)

    class Meta:
        """Meta class."""

        verbose_name = ("Token")
        verbose_name_plural = ("Tokens")

    def save(self, *args, **kwargs):
        """Function for save."""
        if not self.access_key:
            self.access_key = self.generate_key()

        if not self.refresh_key:
            self.refresh_key = self.generate_key()

        self.created = timezone.now()
        self.access_key_expired = self.created + datetime.timedelta(
            minutes=int(settings.LOGIN_EXPIRY))
        self.refresh_key_expired = self.created + datetime.timedelta(
            days=int(settings.REFRESH_EXPIRY))
        return super(UserToken, self).save(*args, **kwargs)

    def generate_key(self):
        """Function to generate key."""
        return binascii.hexlify(os.urandom(20)).decode()
