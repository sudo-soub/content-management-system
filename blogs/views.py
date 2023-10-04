from django.shortcuts import render
from rest_framework import generics, permissions, views
from rest_framework import status
from rest_framework.response import Response
from blogs.models import Blogs
from blogs.serializers import BlogsSerializer


class BlogsGetPostView(views.APIView):
    """This class is used to get details of blogs"""

    def get(self, request, *args, **kwargs):
        """GET request for Blogs"""
        return Blogs.objects.all()


    def post(self, request, *args, **kwargs):
        """POST request to create blogs"""
        serializer = BlogsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class BlogsRetrieveUpdateView(views.APIView):
    """This class is used to retrieve or update a Blog"""
    queryset = Blogs.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """Retrieve method for Blogs"""
        blog_id = self.kwargs['pk']
        return self.queryset.filter(id=blog_id)
    
    def update(self, request, *args, **kwargs):
        """Update method for Blogs"""
        # TBD........
        return Response({}, status=status.HTTP_200_OK)
