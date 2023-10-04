from django.contrib import admin
from blogs.models import Blogs


class BlogsAdmin(admin.ModelAdmin):
    """Admin for Blogs model"""
    list_display = ('user', 'blogname', 'imageurl', 'description')

admin.site.register(Blogs, BlogsAdmin)
