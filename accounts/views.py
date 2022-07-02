from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import AnonymousUser
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializer import UserSerializer
from .utils import get_token, convert_to_seconds
from .permissions import IsUser

# Create your views here.

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                tokens = get_token(user)
                access_time_limit = convert_to_seconds(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"])
                refresh_time_limit = convert_to_seconds(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])

                return Response(data={
                    "access": tokens["access"],
                    "refresh": tokens["refresh"],
                }, status=status.HTTP_200_OK)

            else:
                return Response(data={"status": "error", "message": "Your account has been block for security reasons"}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(data={
                "status": "error",
                "message": "Invalid username or password",
            }, status=status.HTTP_400_BAD_REQUEST)

class GetCurrentUser(APIView):
    http_method_names = ["get", "put"]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(data = serializer.data , status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








