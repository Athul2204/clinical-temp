# authentication/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import CustomTokenObtainPairSerializer, LoginActivitySerializer
from .models import LoginActivity
from .utils import get_client_ip


# ─── Cookie config ────────────────────────────────────────────────
ACCESS_COOKIE  = "access_token"
REFRESH_COOKIE = "refresh_token"
COOKIE_OPTS = dict(httponly=True, secure=False, samesite="Lax")
# Set secure=True in production (HTTPS). False here for local dev.


def _set_auth_cookies(response, access, refresh):
    response.set_cookie(ACCESS_COOKIE,  access,  max_age=5 * 60,         **COOKIE_OPTS)
    response.set_cookie(REFRESH_COOKIE, refresh, max_age=24 * 60 * 60,   **COOKIE_OPTS)


def _clear_auth_cookies(response):
    response.delete_cookie(ACCESS_COOKIE)
    response.delete_cookie(REFRESH_COOKIE)


# ─── LOGIN ────────────────────────────────────────────────────────
class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Returns { user: {...} } in body.
    Tokens go into HttpOnly cookies — JavaScript cannot read them.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = serializer.user

        LoginActivity.objects.create(
            user=user,
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT"),
        )

        response = Response({"user": data["user"]}, status=status.HTTP_200_OK)
        _set_auth_cookies(response, data["access"], data["refresh"])
        return response


# ─── TOKEN REFRESH ────────────────────────────────────────────────
class CookieTokenRefreshView(APIView):
    """
    POST /api/auth/refresh/
    Reads refresh token from HttpOnly cookie, returns new access cookie.
    """
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE)
        if not refresh_token:
            return Response(
                {"detail": "Refresh token missing."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            token = RefreshToken(refresh_token)
            new_access = str(token.access_token)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        response = Response({"detail": "Token refreshed."}, status=status.HTTP_200_OK)
        response.set_cookie(ACCESS_COOKIE, new_access, max_age=5 * 60, **COOKIE_OPTS)
        return response


# ─── ME ───────────────────────────────────────────────────────────
class MeView(APIView):
    """
    GET /api/auth/me/
    Returns logged-in user profile from the HttpOnly cookie session.
    React AuthContext calls this on mount to restore state after refresh.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        staff_profile = getattr(user, "staff_profile", None)
        role = (
            staff_profile.role.lower().replace(" ", "")
            if staff_profile
            else "admin"
        )
        return Response({
            "id":         user.id,
            "username":   user.username,
            "first_name": user.first_name,
            "last_name":  user.last_name,
            "email":      user.email,
            "is_staff":   user.is_staff,
            "role":       role,
        })


# ─── LOGOUT ───────────────────────────────────────────────────────
class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Clears both HttpOnly cookies — safe logout.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"detail": "Logged out."}, status=status.HTTP_200_OK)
        _clear_auth_cookies(response)
        return response


# ─── LOGIN HISTORY ────────────────────────────────────────────────
class LoginActivityView(APIView):
    """
    GET /api/auth/login-history/
    Returns login activity for the current user only.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = LoginActivity.objects.filter(user=request.user)
        serializer = LoginActivitySerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)