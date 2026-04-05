# authentication/cookie_auth.py
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    Reads the access token from the HttpOnly 'access_token' cookie
    instead of the Authorization header.

    This means JavaScript can never read or steal the token — it is
    sent automatically by the browser on every same-origin request.
    """

    def authenticate(self, request):
        raw_token = request.COOKIES.get("access_token")
        if raw_token is None:
            return None  # no cookie → unauthenticated (not an error)
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token