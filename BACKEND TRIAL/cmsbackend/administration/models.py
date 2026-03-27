
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User

# ------------------------------
# Staff Profile
# ------------------------------
class StaffProfile(models.Model):
    ROLE_CHOICES = [
        ("Doctor", "Doctor"),
        ("Receptionist", "Receptionist"),
        ("Lab Technician", "Lab Technician"),
        ("Pharmacist", "Pharmacist"),
        ("Admin", "Admin")
    ]

    id = models.AutoField(primary_key=True)
    staff_code = models.CharField(max_length=20, unique=True, editable=False, db_index=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)  # nullable for migration
    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(r'^\+?\d{9,15}$')],
        null=True,
        blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    qualification = models.CharField(max_length=255, default="Not Specified")
    salary = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=10000)
    joining_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    # Auto-generate Staff Code
    def save(self, *args, **kwargs):
        if not self.staff_code:
            prefix_map = {
                "Doctor": "DOC",
                "Receptionist": "REC",
                "Lab Technician": "LAB",
                "Pharmacist": "PHM",
            }
            prefix = prefix_map.get(self.role, "STF")
            last_staff = StaffProfile.objects.filter(staff_code__startswith=prefix).order_by("-id").first()
            new_number = 1
            if last_staff:
                try:
                    last_number = int(last_staff.staff_code.split("-")[1])
                    new_number = last_number + 1
                except:
                    new_number = 1
            self.staff_code = f"{prefix}-{str(new_number).zfill(3)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.staff_code} - {self.user.username}"


# ------------------------------
# Doctor Profile
# ------------------------------
class DoctorProfile(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    staff = models.OneToOneField(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="doctor_profile",
        null=True,
        blank=True  # nullable for migration
    )
    specialization = models.CharField(max_length=100, default="General")
    consultation_fee = models.PositiveIntegerField(default=500)
    experience_years = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.staff.staff_code if self.staff else 'No Staff'} - {self.specialization}"


# ------------------------------
# Receptionist Profile
# ------------------------------
class ReceptionistProfile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    staff = models.OneToOneField(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="receptionist_profile",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.staff.staff_code if self.staff else 'No Staff'} - Receptionist"


# ------------------------------
# Lab Technician Profile
# ------------------------------
class LabTechnicianProfile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    staff = models.OneToOneField(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="labtech_profile",
        null=True,
        blank=True
    )
    certification_details = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Optional additional certification"
    )

    def __str__(self):
        return f"{self.staff.staff_code if self.staff else 'No Staff'} - Lab Technician"


# ------------------------------
# Pharmacist Profile
# ------------------------------
class PharmacistProfile(models.Model):
    staff = models.OneToOneField(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="pharmacist_profile",
        null=True,
        blank=True
    )
    license_number = models.CharField(max_length=50, unique=True, default="LIC-000")

    def __str__(self):
        return f"{self.staff.staff_code if self.staff else 'No Staff'} - Pharmacist"


# ------------------------------
# Audit Log
# ------------------------------
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
    ]

    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    module = models.CharField(max_length=50, default="General")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    object_id = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.action} - {self.module}"