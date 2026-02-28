from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class Role(models.Model):
    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("DOCTOR", "Doctor"),
        ("RECEPTIONIST", "Receptionist"),
        ("LAB_TECH", "Lab Technician"),
        ("PHARMACIST", "Pharmacist"),
    ]

    rolename = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rolename


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile")
    staff_code = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField()  # REQUIRED BY DOC
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def clean(self):
        if not self.date_of_birth:
            raise ValidationError("Date of birth is required")

    def __str__(self):
        return f"{self.staff_code} - {self.first_name}"


class DoctorProfile(models.Model):
    staff_profile = models.OneToOneField(StaffProfile, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=150)
    certifications = models.CharField(max_length=150)
    specialization = models.CharField(max_length=150)
    experience_years = models.PositiveIntegerField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)


class ReceptionistProfile(models.Model):
    staff_profile = models.OneToOneField(StaffProfile, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=150)
    shift = models.CharField(max_length=50)


class LabTechnicianProfile(models.Model):
    staff_profile = models.OneToOneField(StaffProfile, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=150)
    certifications = models.CharField(max_length=150)
    lab_specialization = models.CharField(max_length=150)


class PharmacistProfile(models.Model):
    staff_profile = models.OneToOneField(StaffProfile, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=150)
    license_number = models.CharField(max_length=100, unique=True)
    certifications = models.CharField(max_length=150)


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    module_name = models.CharField(max_length=100)
    action_type = models.CharField(max_length=100)
    record_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)