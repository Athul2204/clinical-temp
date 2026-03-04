# from rest_framework import serializers
# from .models import (
#     Role, User, StaffProfile,
#     DoctorProfile, ReceptionistProfile,
#     LabTechnicianProfile, PharmacistProfile
# )


# class RoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields = "__all__"


# class UserSerializer(serializers.ModelSerializer):
#     role = serializers.SlugRelatedField(
#         slug_field="rolename",
#         queryset=Role.objects.all()
#     )

#     class Meta:
#         model = User
#         fields = ["id", "username", "email", "role", "is_active"]


# class StaffProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = StaffProfile
#         fields = "__all__"


# class DoctorProfileSerializer(serializers.ModelSerializer):
#     staff_profile = StaffProfileSerializer()

#     class Meta:
#         model = DoctorProfile
#         fields = "__all__"


# class ReceptionistProfileSerializer(serializers.ModelSerializer):
#     staff_profile = StaffProfileSerializer()

#     class Meta:
#         model = ReceptionistProfile
#         fields = "__all__"


# class LabTechnicianProfileSerializer(serializers.ModelSerializer):
#     staff_profile = StaffProfileSerializer()

#     class Meta:
#         model = LabTechnicianProfile
#         fields = "__all__"


# class PharmacistProfileSerializer(serializers.ModelSerializer):
#     staff_profile = StaffProfileSerializer()

#     class Meta:
#         model = PharmacistProfile
#         fields = "__all__"



from rest_framework import serializers
from .models import Role, User, StaffProfile, DoctorProfile, ReceptionistProfile, LabTechnicianProfile, PharmacistProfile, AuditLog
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from datetime import date

# ------------------------------
# Role Serializer
# ------------------------------
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

# ------------------------------
# User Serializer
# ------------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'password', 'role', 'is_active', 'created_at']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

# ------------------------------
# Staff Profile Serializer
# ------------------------------
class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = '__all__'

# ------------------------------
# Doctor Profile Serializer
# ------------------------------
class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'

    def validate(self, data):
        # Minimum age 24 years
        dob = self.context['request'].data.get('date_of_birth')
        if dob:
            age = (date.today() - date.fromisoformat(dob)).days // 365
            if age < 24:
                raise serializers.ValidationError("Doctor must be at least 24 years old")
        return data

# ------------------------------
# Receptionist Serializer
# ------------------------------
class ReceptionistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceptionistProfile
        fields = '__all__'

# ------------------------------
# Lab Technician Serializer
# ------------------------------
class LabTechnicianProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTechnicianProfile
        fields = '__all__'

# ------------------------------
# Pharmacist Serializer
# ------------------------------
class PharmacistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacistProfile
        fields = '__all__'

# ------------------------------
# Audit Log Serializer
# ------------------------------
class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'