from rest_framework import serializers
from .models import (
    Role, User, StaffProfile,
    DoctorProfile, ReceptionistProfile,
    LabTechnicianProfile, PharmacistProfile
)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(
        slug_field="rolename",
        queryset=Role.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "is_active"]


class StaffProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StaffProfile
        fields = "__all__"


class DoctorProfileSerializer(serializers.ModelSerializer):
    staff_profile = StaffProfileSerializer()

    class Meta:
        model = DoctorProfile
        fields = "__all__"


class ReceptionistProfileSerializer(serializers.ModelSerializer):
    staff_profile = StaffProfileSerializer()

    class Meta:
        model = ReceptionistProfile
        fields = "__all__"


class LabTechnicianProfileSerializer(serializers.ModelSerializer):
    staff_profile = StaffProfileSerializer()

    class Meta:
        model = LabTechnicianProfile
        fields = "__all__"


class PharmacistProfileSerializer(serializers.ModelSerializer):
    staff_profile = StaffProfileSerializer()

    class Meta:
        model = PharmacistProfile
        fields = "__all__"