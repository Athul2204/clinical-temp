from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# =========================
# ROLE MODEL
# =========================

class Role(models.Model):
    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("DOCTOR", "Doctor"),
        ("RECEPTIONIST", "Receptionist"),
        ("LAB_TECH", "Lab Technician"),
        ("PHARMACIST", "Pharmacist"),
    ]

    rolename = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        unique=True
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rolename


# =========================
# CUSTOM USER MODEL
# =========================

class User(AbstractUser):
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="users"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


# =========================
# STAFF PROFILE (BASE TABLE)
# =========================

class StaffProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staff_profile"
    )
    staff_code = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    joined_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.first_name:
            raise ValidationError("First name is mandatory.")

    def __str__(self):
        return f"{self.first_name} ({self.staff_code})"


# =========================
# DOCTOR PROFILE
# =========================

class DoctorProfile(models.Model):
    staff_profile = models.OneToOneField(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="doctor_profile"
    )
    specialization = models.CharField(max_length=150, blank=True)
    qualification = models.CharField(max_length=150, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Dr. {self.staff_profile.first_name}"


# =========================
# RECEPTIONIST PROFILE
# =========================

class ReceptionistProfile(models.Model):
    staff_profile = models.OneToOneField(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="receptionist_profile"
    )
    shift = models.CharField(max_length=50, blank=True)
    qualification = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.staff_profile.first_name


# =========================
# LAB TECHNICIAN PROFILE
# =========================

class LabTechnicianProfile(models.Model):
    staff_profile = models.OneToOneField(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="lab_technician_profile"
    )
    lab_specialization = models.CharField(max_length=150, blank=True)
    certification = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.staff_profile.first_name


# =========================
# PHARMACIST PROFILE
# =========================

class PharmacistProfile(models.Model):
    staff_profile = models.OneToOneField(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="pharmacist_profile"
    )
    license_number = models.CharField(max_length=100, unique=True)
    certification = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.staff_profile.first_name


# =========================
# AUDIT LOG (ADMIN MONITORING)
# =========================

class AuditLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="audit_logs"
    )
    module_name = models.CharField(max_length=100)
    action_type = models.CharField(max_length=100)
    record_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action_type}"