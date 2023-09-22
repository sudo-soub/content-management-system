import os
import binascii

from django.shortcuts import render
from rest_framework import generics, permissions, views
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import authenticate
from common.models import UserToken
from datetime import timezone

class CreateAccount(views.APIView):
    """This class is used to create new users"""

    def post(self, request, *args, **kwargs):
        """Function for POST request"""
        
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if not email or not password:
            # if data is not present in the request
            msg = "Email and password are required!"
            return Response({"message": msg}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).count():
            # check if user already exists
            msg = "User {} already exists!".format(email)
            return Response({"message": msg}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            try:
                user = User.objects.create_user(email, email, password)

                if user:
                    user.save()
                    msg = "User {} created successfully".format(email)
                    return Response(
                        {"message": msg}, status=status.HTTP_201_CREATED
                    )
            
            except:
                err = "Something went wrong! Please try again!"
                return Response(
                    {"message": err}, status=status.HTTP_400_BAD_REQUEST
                )


class UserLogin(views.APIView):
    """This class is used for user login"""

    def post(self, request, *args, **kwargs):
        """Function for POST request."""
        data = request.data
        username = data["username"]
        password = data["password"]

        # Check if there is the user is authenticated or not.
        user = authenticate(username=username, password=password)

        if user is not None:
            # Check if there is token created for the user or not.
            # If not created then create, if created then check the expiry time
            # check if the user is super admin or has any groups or not.
            groups = user.groups.all()
            
            if not groups:
                if not user.is_staff:
                    msg = "User is not authorised, please contact admin."
                    return Response(
                        {"detail": msg}, status=status.HTTP_401_UNAUTHORIZED
                    )

            token_obj = UserToken.objects.create(user_id=user.id)
            msg = {
                "access_key": token_obj.access_key,
                "access_key_expired": token_obj.access_key_expired,
                "refresh_key": token_obj.refresh_key,
                "refresh_key_expired": token_obj.refresh_key_expired,
            }
            return Response(msg, status=status.HTTP_201_CREATED)
        
        else:
            msg = {"detail": "Username or Password is incorrect"}
            return Response(msg, status=status.HTTP_401_UNAUTHORIZED)


class RefreshToken(views.APIView):
    """This class is used to update the access token using refresh token."""

    authentication_classes=[]
    permission_classes = [permissions.AllowAny]


    def generate_key(self):
        """Function to generate key."""
        return binascii.hexlify(os.urandom(20)).decode()


    def post(self, request, *args, **kwargs):
        """Function for POST request."""
        access_key = request.data.get("access_key")
        refresh_key = request.data.get("refresh_key")
        
        if not access_key or not refresh_key:
            msg = "access_key or refresh_key is required and cannot be empty."
            return Response(
                {"detail": msg}, status=status.HTTP_400_BAD_REQUEST
            )
        token_obj = UserToken.objects.filter(
            access_key=access_key).values().first()
        
        if token_obj:
            if token_obj["refresh_key"] != refresh_key:
                return Response(
                    {"detail": "refresh_key mismatch."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if token_obj["refresh_key_expired"] > timezone.now():
                user_id = token_obj['user_id']
                created_token = UserToken.objects.create(user_id=user_id)

                text = "Access Token Refreshed Successfully ! "
                text += "Please find new Access Token and Refresh Token."
                msg = {
                    "message": text,
                    "access_key": created_token.access_key,
                    "access_key_expired": created_token.access_key_expired,
                    "refresh_key": created_token.refresh_key,
                    "refresh_key_expired": created_token.refresh_key_expired,
                }
                return Response(msg, status=status.HTTP_200_OK)
            
            else:
                UserToken.objects.filter(access_key=access_key).delete()
                return Response(
                    {"detail": "refresh_key is expired, please login again."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        else:
            return Response(
                {"detail": "access_key not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
