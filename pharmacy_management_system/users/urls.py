from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CustomTokenObtainPairView, UserDetails, UserRegistrationView

urlpatterns = [
    # Registration Endpoint
    path("register/", UserRegistrationView.as_view(), name="register"),
    # Login (Token Obtain)
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("me/", UserDetails.as_view(), name="token_obtain_pair"),
    # Token Refresh
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
