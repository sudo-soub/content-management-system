import os
import binascii
import jwt

from django.shortcuts import render
from rest_framework import generics, permissions, views
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import authenticate
from common.models import UserToken
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail


class VerifyEmailView(views.APIView):
    """This class is used to verify email before creating account"""

    def post(self, request, *args, **kwargs):
        """Function for PPOST request"""

        email = request.data.get("email", None)
        token = request.data.get("token", None)
        base_url = request.data.get("base_url", None)

        if not email:
            err = "Email is required!"
            return Response({"message": err}, status=status.HTTP_400_BAD_REQUEST)

        if not token:
            err = "Unique token not found!"
            return Response({"message": err}, status=status.HTTP_400_BAD_REQUEST)

        if not base_url:
            err = "Base URL not provided!"
            return Response({"message": err}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).count():
            # check if user already exists
            msg = "Email {} already exists!".format(email)
            return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            secret = settings.JWT_SECRET
            print(secret)
            encoded = jwt.encode(
                {"email": email, "token": token}, secret, algorithm="HS256"
            )
            # encoded = "sdncjk543"
            print(encoded)
            subject = 'Email verification'
            body = "You are receiving this email to verify this email address "\
            +"to our CMS portal."\
            "\nYou can use this email address to recover your password incase "\
            +"you forget it in the future."\
            "\nPlease click on the given link to verify this email and choose "\
            +"an appropriate username and a strong password."\
            "\n\n{}/signup?verify={}"\
            "\n\n\nHappy blogging! :)".format(base_url, encoded)
            # print(body)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            result = send_mail( subject, body, email_from, recipient_list )
            print("result", result)
            msg = "Email sent successfully!"
            return Response({"message": msg}, status=status.HTTP_200_OK)
        
        except:
            err = "Something went wrong!"
            return Response({"error": err}, status=status.HTTP_400_BAD_REQUEST)



class CreateAccount(views.APIView):
    """This class is used to create new users"""

    def post(self, request, *args, **kwargs):
        """Function for POST request"""

        email = request.data.get("email", None)
        password = request.data.get("password", None)
        username = request.data.get("username", None)
        firstname = request.data.get("firstname", "")
        lastname = request.data.get("lastname", "")

        if not email or not password or not username:
            # if data is not present in the request
            err = "All the fields are required!"
            return Response(
                {
                    "error": err, "type": 1
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).count():
            # check if username already exists
            err = "Username {} already taken!".format(username)
            return Response(
                {
                    "error": err, "type": 2
                }, status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).count():
            # check if user already exists
            msg = "Email {} already exists!".format(email)
            return Response(
                {
                    "error": msg, "type": 3
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        else:
            try:
                user = User.objects.create_user(username, email, password)

                if user:
                    user.first_name = firstname
                    user.last_name = lastname
                    user.save()
                    msg = "User {} created successfully".format(username)
                    return Response(
                        {"message": msg}, status=status.HTTP_201_CREATED
                    )
            
            except:
                err = "Something went wrong! Please try again!"
                return Response(
                    {"error": err}, status=status.HTTP_400_BAD_REQUEST
                )


class UserLogin(views.APIView):
    """This class is used for user login"""

    def post(self, request, *args, **kwargs):
        """Function for POST request."""
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        if not username or not password:
            err = "Username and password are required!"
            return Response({"error": err}, status=status.HTTP_400_BAD_REQUEST)

        # Check if there is the user is authenticated or not.
        user = authenticate(username=username, password=password)

        if user is not None:
            # Check if there is token created for the user or not.
            # If not created then create, if created then check the expiry time
            token_obj = UserToken.objects.create(user_id=user.id)
            msg = {
                "access_key": token_obj.access_key,
                "access_key_expired": token_obj.access_key_expired,
                "refresh_key": token_obj.refresh_key,
                "refresh_key_expired": token_obj.refresh_key_expired,
                "username": user.username
            }
            return Response(msg, status=status.HTTP_201_CREATED)
        
        else:
            msg = {"error": "Username or Password is incorrect"}
            return Response(msg, status=status.HTTP_401_UNAUTHORIZED)


class RefreshToken(views.APIView):
    """This class is used to update the access token using refresh token."""

    def generate_key(self):
        """Function to generate key."""
        return binascii.hexlify(os.urandom(20)).decode()

    def post(self, request, *args, **kwargs):
        """Function for POST request."""
        access_key = request.data.get("access_key")
        refresh_key = request.data.get("refresh_key")
        username = request.data.get("username")
        
        if not access_key or not refresh_key:
            err = "access_key or refresh_key is required and cannot be empty."
            return Response(
                {"error": err}, status=status.HTTP_400_BAD_REQUEST
            )
        token_obj = UserToken.objects.filter(
            access_key=access_key).values().first()
        
        if token_obj:
            if token_obj["refresh_key"] != refresh_key:
                return Response(
                    {"error": "refresh_key mismatch."},
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
                    "username": username
                }
                return Response(msg, status=status.HTTP_200_OK)
            
            else:
                UserToken.objects.filter(access_key=access_key).delete()
                return Response(
                    {"error": "refresh_key is expired, please login again."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        else:
            return Response(
                {"error": "access_key not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
