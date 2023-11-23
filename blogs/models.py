from django.db import models
from django.contrib.auth.models import User


class Blogs(models.Model):
    """Model to store blog details"""

    user = models.ForeignKey(User, blank=True, null=True,
        on_delete=models.DO_NOTHING)
    blogname = models.CharField(max_length=255)
    blog_data = models.TextField(default="")

    class Meta:
        verbose_name = ("Blog")
        verbose_name_plural = ("Blogs")
