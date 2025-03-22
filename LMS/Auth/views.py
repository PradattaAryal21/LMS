from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from Auth.services import UserService
from rest_framework import status, generics, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny  
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializer import *
from rest_framework.decorators import action


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]  # Disable authentication for login view

    def post(self, request):
        service = UserService()
        result = service.login(request.data)
        if not result:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            
        # Generate JWT tokens (access and refresh tokens)
        refresh = RefreshToken.for_user(result)

        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
         
        return Response({
            "id": str(result.userId),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, status=status.HTTP_200_OK)

class RegisterUserView(APIView):
    permission_classes = [AllowAny]  # Disable authentication for registration view

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            # If the serializer is valid, register the user using the UserService
            service = UserService()
            user = service.register_user(serializer.validated_data)

            # Serialize the user object to return in the response
            user_serializer = UserSerializer(user)

            # Return a success response with the user data
            return Response({"message": "User created successfully", "user": user_serializer.data}, status=status.HTTP_201_CREATED)

        # If there are validation errors, return a 400 response with the error details
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 