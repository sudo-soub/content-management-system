from rest_framework import serializers
from blogs.models import Blogs


class BlogsSerializer(serializers.ModelSerializer):
    """Serializer for Blogs model"""
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Blogs
        fields = '__all__'
