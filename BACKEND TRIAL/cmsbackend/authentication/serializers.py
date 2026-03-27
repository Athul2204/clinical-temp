from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import LoginActivity


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT Token Serializer
    Adds extra user data inside token
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['is_staff'] = user.is_staff
        token['email'] = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        role = self.user.staff_profile.role.lower().replace(" ", "")

        data['user'] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "is_staff": self.user.is_staff,
            "role": role
        }

        return data


class LoginActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = LoginActivity
        fields = "__all__"
        read_only_fields = ["login_time"]