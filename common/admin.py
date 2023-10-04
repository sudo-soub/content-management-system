from django.contrib import admin
from common.models import UserToken


class UserTokenAdmin(admin.ModelAdmin):
    """Admin for UserToken model"""
    list_display = (
        'user', 'access_key', 'refresh_key', 'created', 'access_key_expired',
        'refresh_key_expired'    
    )

admin.site.register(UserToken, UserTokenAdmin)