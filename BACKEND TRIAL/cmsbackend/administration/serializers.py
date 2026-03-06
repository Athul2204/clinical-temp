from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from datetime import date

from .models import (
    StaffProfile,
    DoctorProfile,
    ReceptionistProfile,
    LabTechnicianProfile,
    PharmacistProfile,
    AuditLog
)


# ------------------------------
# USER SERIALIZER
# ------------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active']
        read_only_fields = ['id']

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        try:
            password = validated_data.pop('password')
            user = User(**validated_data)
            user.set_password(password)
            user.full_clean()
            user.save()
            return user
        except Exception as e:
            raise serializers.ValidationError({"detail": f"User creation failed: {str(e)}"})


# ------------------------------
# BASE STAFF VALIDATOR
# ------------------------------
def validate_staff_role(staff, expected_role):
    if not staff:
        raise serializers.ValidationError("Staff is required.")
    if staff.role != expected_role:
        raise serializers.ValidationError(f"Assigned staff is not a {expected_role}.")


# ------------------------------
# STAFF PROFILE SERIALIZER
# ------------------------------
class StaffProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested User serializer

    class Meta:
        model = StaffProfile
        fields = '__all__'
        read_only_fields = ['staff_code', 'created_at', 'updated_at']

    def validate_salary(self, value):
        if value <= 0:
            raise serializers.ValidationError("Salary must be positive.")
        if value > 1000000:
            raise serializers.ValidationError("Salary exceeds allowed limit.")
        return value

    def validate_joining_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Joining date cannot be in the future.")
        return value

    def validate_date_of_birth(self, value):
        if value:
            if value > date.today():
                raise serializers.ValidationError("Date of birth cannot be in the future.")
            age = (date.today() - value).days // 365
            if age < 18:
                raise serializers.ValidationError("Staff must be at least 18 years old.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        staff = StaffProfile.objects.create(user=user, **validated_data)
        return staff

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance=instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        return super().update(instance, validated_data)


# ------------------------------
# DOCTOR PROFILE SERIALIZER
# ------------------------------
class DoctorProfileSerializer(serializers.ModelSerializer):
    staff = StaffProfileSerializer()

    class Meta:
        model = DoctorProfile
        fields = '__all__'

    def validate(self, data):
        staff = data.get("staff")
        validate_staff_role(staff, "Doctor")

        consultation_fee = data.get("consultation_fee")
        if consultation_fee is None or consultation_fee <= 0:
            raise serializers.ValidationError("Consultation fee must be positive.")

        experience_years = data.get("experience_years")
        if experience_years is None or experience_years < 0:
            raise serializers.ValidationError("Experience cannot be negative.")
        if experience_years > 60:
            raise serializers.ValidationError("Experience cannot exceed 60 years.")

        return data

    @transaction.atomic
    def create(self, validated_data):
        staff_data = validated_data.pop('staff')
        staff_serializer = StaffProfileSerializer(data=staff_data)
        staff_serializer.is_valid(raise_exception=True)
        staff = staff_serializer.save()
        doctor = DoctorProfile.objects.create(staff=staff, **validated_data)
        return doctor

    @transaction.atomic
    def update(self, instance, validated_data):
        staff_data = validated_data.pop('staff', None)
        if staff_data:
            staff_serializer = StaffProfileSerializer(instance=instance.staff, data=staff_data, partial=True)
            staff_serializer.is_valid(raise_exception=True)
            staff_serializer.save()
        return super().update(instance, validated_data)


# ------------------------------
# RECEPTIONIST PROFILE SERIALIZER
# ------------------------------
class ReceptionistProfileSerializer(serializers.ModelSerializer):
    staff = StaffProfileSerializer()

    class Meta:
        model = ReceptionistProfile
        fields = '__all__'

    def validate(self, data):
        validate_staff_role(data.get('staff'), "Receptionist")
        return data

    @transaction.atomic
    def create(self, validated_data):
        staff_data = validated_data.pop('staff')
        staff_serializer = StaffProfileSerializer(data=staff_data)
        staff_serializer.is_valid(raise_exception=True)
        staff = staff_serializer.save()
        return ReceptionistProfile.objects.create(staff=staff, **validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        staff_data = validated_data.pop('staff', None)
        if staff_data:
            staff_serializer = StaffProfileSerializer(instance=instance.staff, data=staff_data, partial=True)
            staff_serializer.is_valid(raise_exception=True)
            staff_serializer.save()
        return super().update(instance, validated_data)


# ------------------------------
# LAB TECHNICIAN PROFILE SERIALIZER
# ------------------------------
class LabTechnicianProfileSerializer(serializers.ModelSerializer):
    staff = StaffProfileSerializer()

    class Meta:
        model = LabTechnicianProfile
        fields = '__all__'

    def validate(self, data):
        validate_staff_role(data.get('staff'), "Lab Technician")
        return data

    @transaction.atomic
    def create(self, validated_data):
        staff_data = validated_data.pop('staff')
        staff_serializer = StaffProfileSerializer(data=staff_data)
        staff_serializer.is_valid(raise_exception=True)
        staff = staff_serializer.save()
        return LabTechnicianProfile.objects.create(staff=staff, **validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        staff_data = validated_data.pop('staff', None)
        if staff_data:
            staff_serializer = StaffProfileSerializer(instance=instance.staff, data=staff_data, partial=True)
            staff_serializer.is_valid(raise_exception=True)
            staff_serializer.save()
        return super().update(instance, validated_data)


# ------------------------------
# PHARMACIST PROFILE SERIALIZER
# ------------------------------
class PharmacistProfileSerializer(serializers.ModelSerializer):
    staff = StaffProfileSerializer()

    class Meta:
        model = PharmacistProfile
        fields = '__all__'

    def validate(self, data):
        validate_staff_role(data.get('staff'), "Pharmacist")
        return data

    @transaction.atomic
    def create(self, validated_data):
        staff_data = validated_data.pop('staff')
        staff_serializer = StaffProfileSerializer(data=staff_data)
        staff_serializer.is_valid(raise_exception=True)
        staff = staff_serializer.save()
        return PharmacistProfile.objects.create(staff=staff, **validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        staff_data = validated_data.pop('staff', None)
        if staff_data:
            staff_serializer = StaffProfileSerializer(instance=instance.staff, data=staff_data, partial=True)
            staff_serializer.is_valid(raise_exception=True)
            staff_serializer.save()
        return super().update(instance, validated_data)


# ------------------------------
# AUDIT LOG SERIALIZER (READ ONLY)
# ------------------------------
class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'
        read_only_fields = '__all__'