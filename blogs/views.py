from rest_framework import permissions, views
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from blogs.models import Blogs
from blogs.serializers import BlogsSerializer
from django.conf import settings
from django.contrib.auth.models import User
from cms.auth import UserTokenAuthentication


class BlogsGetPostView(views.APIView):
    """This class is used to get details of blogs"""
    authentication_classes = [UserTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """GET request for Blogs"""
        blogs = Blogs.objects.values(
            "id", "blogname", "imageurl", "description", "article_body",
            "user__username", "user__first_name", "user__last_name"
        )
        return Response({"message": blogs}, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        """POST request to create blogs"""
        username = self.request.user
        print(username)
        user = User.objects.get(username=username).pk
        request.data["user"] = user
        serializer = BlogsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class BlogsRetrieveUpdateView(ModelViewSet):
    """This class is used to retrieve or update a Blog"""
    authentication_classes = [UserTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Blogs.objects.values(
        "article_body", "blogname", "description", "imageurl", "user__username",
        "user__first_name", "user__last_name"
    )

    def retrieve(self, request, *args, **kwargs):
        """Retrieve method for Blogs"""
        blog_id = self.kwargs['pk']
        result = self.queryset.filter(id=blog_id).first()
        return Response({"message": result}, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        """Update method for Blogs"""
        # TBD........
        return Response({}, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        """Method to delete blog"""
        user = self.request.user
        blog_id = self.kwargs['pk']
        
        if not user:
            err = "User not found in request!"
            return Response({"error": err}, status=status.HTTP_400_BAD_REQUEST)
        
        if not blog_id:
            err = "Please provide blog id!"
            return Response({"error": err}, status=status.HTTP_400_BAD_REQUEST)
        
        user_obj = User.objects.filter(username=user).first()
        result = Blogs.objects.filter(id=blog_id, user=user_obj).delete()

        if not result:
            err = "Unauthorised access!"
            return Response({"error": err}, status=status.HTTP_403_FORBIDDEN)
        
        return Response({"message": result}, status=status.HTTP_200_OK)


class GetUpdateBlogsByUser(views.APIView):
    """This class is used to get and update blogs by user"""
    authentication_classes = [UserTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Method for GET request"""
        user = self.request.user
        queryset = Blogs.objects.filter(user__username=user).values(
            "article_body", "blogname", "description", "imageurl", "user__username",
            "user__first_name", "user__last_name", "id"
        )

        return Response(queryset, status=status.HTTP_200_OK)
    
