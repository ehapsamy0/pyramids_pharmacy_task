from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from users.permissions import IsPatient
from users.permissions import IsPharmacist

from .models import User
from .serializers import UserRegistrationSerializer
from .serializers import UserSerializer

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Validate and save the user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens for the new user
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # Return the user data and the access/refresh tokens
        return Response(
            {
                "user": serializer.data,  # User data
                "refresh": str(refresh),  # Refresh token
                "access": str(access),  # Access token
            },
            status=status.HTTP_201_CREATED,
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    class CustomTokenObtainPairViewOutputSerializer(serializers.Serializer):
        refresh = serializers.CharField()
        access = serializers.CharField()
        role = serializers.CharField()
        username = serializers.CharField()

    class TokenSerializer(TokenObtainPairSerializer):
        @classmethod
        def get_token(cls, user: User):
            token = super().get_token(user)
            # Adding custom claims (role and username)
            token["name"] = user.name
            token["username"] = user.username
            token["role"] = (
                "admin"
                if user.is_admin
                else "patient"
                if user.is_patient
                else "pharmacist"
            )
            return token

    serializer_class = TokenSerializer

    @extend_schema(
        request=TokenObtainPairSerializer,
        responses=CustomTokenObtainPairViewOutputSerializer,
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(username=request.data["username"])
        # Adding role and username in response
        response.data.update(
            {
                "role": "admin"
                if user.is_admin
                else "patient"
                if user.is_patient
                else "pharmacist",
                "username": user.username,
            }
        )
        return response


class UserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a User Data.
        """
        return Response(
            UserSerializer(instance=request.user).data,
            status=status.HTTP_200_OK,
        )
