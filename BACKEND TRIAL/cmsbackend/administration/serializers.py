from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from datetime import date

from .models import (
    StaffProfile, DoctorProfile, ReceptionistProfile,
    LabTechnicianProfile, PharmacistProfile, AuditLog
)

# ─── CONFIG ───────────────────────────────────────────────
ROLE_MIN_AGE = {
    "Doctor": 25,
    "Receptionist": 21,
    "Lab Technician": 22,
    "Pharmacist": 23,
    "Admin": 21
}

def calculate_age(dob):
    if not dob:
        return 0
    return (date.today() - dob).days // 365


# ─── USER SERIALIZER ──────────────────────────────────────
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        read_only_fields = ['id']
        extra_kwargs = {'username': {'required': False}}

    def create(self, validated_data):
        pwd = validated_data.pop("password", None)

        if not validated_data.get('username'):
            base = validated_data.get('email', '').split('@')[0] or 'user'
            username = base
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base}{counter}"
                counter += 1
            validated_data['username'] = username

        user = User(**validated_data)

        if pwd:
            user.set_password(pwd)
        else:
            user.set_unusable_password()

        user.save()
        return user

    def update(self, instance, validated_data):
        pwd = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if pwd:
            instance.set_password(pwd)

        instance.save()
        return instance


# ─── STAFF PROFILE SERIALIZER ─────────────────────────────
class StaffProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StaffProfile
        fields = "__all__"
        read_only_fields = ['staff_code', 'created_at', 'updated_at']

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop("user")

        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        dob = validated_data.get("date_of_birth")
        role = validated_data.get("role")

        if dob and calculate_age(dob) < ROLE_MIN_AGE.get(role, 21):
            raise serializers.ValidationError({
                "date_of_birth": f"{role} must be at least {ROLE_MIN_AGE.get(role, 21)} years old."
            })

        return StaffProfile.objects.create(user=user, **validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)

        if user_data:
            UserSerializer().update(instance.user, user_data)

        dob = validated_data.get("date_of_birth", instance.date_of_birth)
        role = validated_data.get("role", instance.role)

        if dob and calculate_age(dob) < ROLE_MIN_AGE.get(role, 21):
            raise serializers.ValidationError({
                "date_of_birth": f"{role} must be at least {ROLE_MIN_AGE.get(role, 21)} years old."
            })

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


# ─── ROLE SERIALIZERS (FINAL FIX) ─────────────────────────
# ✅ SHOW staff details
# ❌ DO NOT allow updating staff

class DoctorProfileSerializer(serializers.ModelSerializer):
    staff = StaffProfileSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = "__all__"


class ReceptionistProfileSerializer(serializers.ModelSerializer):
    staff = StaffProfileSerializer(read_only=True)

    class Meta:
        model = ReceptionistProfile
        fields = "__all__"


class LabTechnicianProfileSerializer(serializers.ModelSerializer):
    staff = StaffProfileSerializer(read_only=True)

    class Meta:
        model = LabTechnicianProfile
        fields = "__all__"


class PharmacistProfileSerializer(serializers.ModelSerializer):
    staff = StaffProfileSerializer(read_only=True)

    class Meta:
        model = PharmacistProfile
        fields = "__all__"


# ─── AUDIT LOG SERIALIZER ────────────────────────────────
class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = AuditLog
        fields = "__all__"