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
# CONSTANTS (BUSINESS RULES)
# ------------------------------

ROLE_MIN_AGE = {
    "Doctor": 25,
    "Receptionist": 21,
    "Lab Technician": 22,
    "Pharmacist": 23
}

MAX_SALARY_LIMIT = 1000000


# ------------------------------
# HELPER FUNCTIONS
# ------------------------------

def calculate_age(dob):
    return (date.today() - dob).days // 365


def validate_staff_role(staff, expected_role):
    if not staff:
        raise serializers.ValidationError("Staff is required.")

    role = staff.get("role")

    if role != expected_role:
        raise serializers.ValidationError(
            f"Assigned staff must have role '{expected_role}'."
        )


# ------------------------------
# USER SERIALIZER
# ------------------------------

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active']
        read_only_fields = ['id']

    def validate_username(self, value):

        if len(value) < 4:
            raise serializers.ValidationError(
                "Username must contain at least 4 characters."
            )

        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "Username already exists."
            )

        return value

    def validate_email(self, value):

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "Email already exists."
            )

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

            raise serializers.ValidationError(
                {"detail": f"User creation failed: {str(e)}"}
            )


# ------------------------------
# STAFF PROFILE SERIALIZER
# ------------------------------

class StaffProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = StaffProfile
        fields = '__all__'
        read_only_fields = ['staff_code', 'created_at', 'updated_at']

    def validate(self, data):

        role = data.get("role")
        dob = data.get("date_of_birth")
        salary = data.get("salary")
        joining_date = data.get("joining_date")
        qualification = data.get("qualification")

        # --------------------
        # DATE OF BIRTH VALIDATION
        # --------------------

        if dob:

            if dob > date.today():
                raise serializers.ValidationError(
                    {"date_of_birth": "Date of birth cannot be in the future."}
                )

            age = calculate_age(dob)

            min_age = ROLE_MIN_AGE.get(role, 21)

            if age < min_age:
                raise serializers.ValidationError(
                    {"date_of_birth": f"{role} must be at least {min_age} years old."}
                )

        # --------------------
        # SALARY VALIDATION
        # --------------------

        if salary:

            if salary <= 0:
                raise serializers.ValidationError(
                    {"salary": "Salary must be greater than zero."}
                )

            if salary > MAX_SALARY_LIMIT:
                raise serializers.ValidationError(
                    {"salary": "Salary exceeds allowed limit."}
                )

        # --------------------
        # JOINING DATE VALIDATION
        # --------------------

        if joining_date:

            if joining_date > date.today():
                raise serializers.ValidationError(
                    {"joining_date": "Joining date cannot be in the future."}
                )

        # --------------------
        # QUALIFICATION VALIDATION
        # --------------------

        if qualification:

            if len(qualification.strip()) < 3:
                raise serializers.ValidationError(
                    {"qualification": "Qualification must contain valid text."}
                )

        return data

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

            user_serializer = UserSerializer(
                instance=instance.user,
                data=user_data,
                partial=True
            )

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

        if consultation_fee <= 0:
            raise serializers.ValidationError(
                {"consultation_fee": "Consultation fee must be positive."}
            )

        experience = data.get("experience_years")

        if experience < 0:
            raise serializers.ValidationError(
                {"experience_years": "Experience cannot be negative."}
            )

        if experience > 60:
            raise serializers.ValidationError(
                {"experience_years": "Experience exceeds realistic limit."}
            )

        # --------------------
        # EXPERIENCE vs AGE VALIDATION
        # --------------------

        dob = staff.get("date_of_birth")

        if dob:

            age = calculate_age(dob)

            if experience > age - 23:
                raise serializers.ValidationError(
                    {"experience_years": "Experience does not match doctor's age."}
                )

        return data

    @transaction.atomic
    def create(self, validated_data):

        staff_data = validated_data.pop('staff')

        staff_serializer = StaffProfileSerializer(data=staff_data)

        staff_serializer.is_valid(raise_exception=True)

        staff = staff_serializer.save()

        doctor = DoctorProfile.objects.create(
            staff=staff,
            **validated_data
        )

        return doctor

    @transaction.atomic
    def update(self, instance, validated_data):

        staff_data = validated_data.pop('staff', None)

        if staff_data:

            staff_serializer = StaffProfileSerializer(
                instance=instance.staff,
                data=staff_data,
                partial=True
            )

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

        return ReceptionistProfile.objects.create(
            staff=staff,
            **validated_data
        )

    @transaction.atomic
    def update(self, instance, validated_data):

        staff_data = validated_data.pop('staff', None)

        if staff_data:

            staff_serializer = StaffProfileSerializer(
                instance=instance.staff,
                data=staff_data,
                partial=True
            )

            staff_serializer.is_valid(raise_exception=True)

            staff_serializer.save()

        return super().update(instance, validated_data)


# ------------------------------
# LAB TECHNICIAN SERIALIZER
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

        return LabTechnicianProfile.objects.create(
            staff=staff,
            **validated_data
        )

    @transaction.atomic
    def update(self, instance, validated_data):

        staff_data = validated_data.pop('staff', None)

        if staff_data:

            staff_serializer = StaffProfileSerializer(
                instance=instance.staff,
                data=staff_data,
                partial=True
            )

            staff_serializer.is_valid(raise_exception=True)

            staff_serializer.save()

        return super().update(instance, validated_data)


# ------------------------------
# PHARMACIST SERIALIZER
# ------------------------------

class PharmacistProfileSerializer(serializers.ModelSerializer):

    staff = StaffProfileSerializer()

    class Meta:
        model = PharmacistProfile
        fields = '__all__'

    def validate_license_number(self, value):

        if len(value) < 5:
            raise serializers.ValidationError(
                "Invalid pharmacist license number."
            )

        return value

    def validate(self, data):

        validate_staff_role(data.get('staff'), "Pharmacist")

        return data

    @transaction.atomic
    def create(self, validated_data):

        staff_data = validated_data.pop('staff')

        staff_serializer = StaffProfileSerializer(data=staff_data)

        staff_serializer.is_valid(raise_exception=True)

        staff = staff_serializer.save()

        return PharmacistProfile.objects.create(
            staff=staff,
            **validated_data
        )

    @transaction.atomic
    def update(self, instance, validated_data):

        staff_data = validated_data.pop('staff', None)

        if staff_data:

            staff_serializer = StaffProfileSerializer(
                instance=instance.staff,
                data=staff_data,
                partial=True
            )

            staff_serializer.is_valid(raise_exception=True)

            staff_serializer.save()

        return super().update(instance, validated_data)


# ------------------------------
# AUDIT LOG SERIALIZER
# ------------------------------

class AuditLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuditLog
        fields = '__all__'
        read_only_fields = '__all__'