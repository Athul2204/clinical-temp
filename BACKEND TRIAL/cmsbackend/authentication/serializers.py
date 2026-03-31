# from rest_framework import serializers
# from django.contrib.auth.models import User
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from .models import LoginActivity


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     """
#     Custom JWT Token Serializer
#     Adds extra user data inside token
#     """

#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         token['username'] = user.username
#         token['is_staff'] = user.is_staff
#         token['email'] = user.email

#         return token

#     def validate(self, attrs):
#         data = super().validate(attrs)
#         role = self.user.staff_profile.role.lower().replace(" ", "")

#         data['user'] = {
#             "id": self.user.id,
#             "username": self.user.username,
#             "email": self.user.email,
#             "is_staff": self.user.is_staff,
#             "role": role
#         }

#         return data


# class LoginActivitySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = LoginActivity
#         fields = "__all__"
#         read_only_fields = ["login_time"]


from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import LoginActivity


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT Token Serializer
    Supports both staff users with StaffProfile and Django superusers.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom fields to token
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        token['email'] = user.email

        # Determine role safely
        staff_profile = getattr(user, "staff_profile", None)
        role = staff_profile.role.lower().replace(" ", "") if staff_profile else "admin"
        token['role'] = role

        return token

    def validate(self, attrs):
        """
        Validates user credentials and adds custom user info to response.
        """
        data = super().validate(attrs)
        user = self.user

        # Safe role access
        staff_profile = getattr(user, "staff_profile", None)
        role = staff_profile.role.lower().replace(" ", "") if staff_profile else "admin"

        data['user'] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
            "role": role
        }

        return data


class LoginActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for login activity logs
    """
    class Meta:
        model = LoginActivity
        fields = "__all__"
        read_only_fields = ["login_time"]