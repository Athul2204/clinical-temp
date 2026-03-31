from django.db import models, transaction
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date


def calculate_age(dob):
    return (date.today() - dob).days // 365 if dob else 0


# ─────────────────────────────────────────────
# Staff Profile
# ─────────────────────────────────────────────
class StaffProfile(models.Model):

    ROLE_CHOICES = [
        ("Doctor", "Doctor"),
        ("Receptionist", "Receptionist"),
        ("Lab Technician", "Lab Technician"),
        ("Pharmacist", "Pharmacist"),
        ("Admin", "Admin"),
    ]

    id = models.AutoField(primary_key=True)
    staff_code = models.CharField(max_length=20, unique=True, editable=False, db_index=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    phone = models.CharField(
        max_length=15, unique=True,
        validators=[RegexValidator(r'^\+?\d{9,15}$')],
        null=True, blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    qualification = models.CharField(max_length=255, default="Not Specified")
    salary = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=10000)
    joining_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Only validate fields that are set
        if self.date_of_birth:
            if self.date_of_birth > date.today():
                raise ValidationError({"date_of_birth": "DOB cannot be in the future."})
            role_min_age = {
                "Doctor": 25, "Receptionist": 21,
                "Lab Technician": 22, "Pharmacist": 23, "Admin": 21,
            }
            if self.role:
                age = calculate_age(self.date_of_birth)
                min_age = role_min_age.get(self.role, 21)
                if age < min_age:
                    raise ValidationError({
                        "date_of_birth": f"{self.role} must be at least {min_age} years old."
                    })

        if self.salary is not None:
            if self.salary <= 0:
                raise ValidationError({"salary": "Salary must be positive."})
            if self.salary > 1_000_000:
                raise ValidationError({"salary": "Salary exceeds the allowed limit."})

        if self.joining_date and self.joining_date > date.today():
            raise ValidationError({"joining_date": "Joining date cannot be in the future."})

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.staff_code:
            with transaction.atomic():
                prefix_map = {
                    "Doctor": "DOC", "Receptionist": "REC",
                    "Lab Technician": "LAB", "Pharmacist": "PHM", "Admin": "ADM",
                }
                prefix = prefix_map.get(self.role, "STF")
                last = (
                    StaffProfile.objects
                    .select_for_update()
                    .filter(staff_code__startswith=prefix)
                    .order_by("-id")
                    .first()
                )
                new_number = 1
                if last and last.staff_code:
                    try:
                        new_number = int(last.staff_code.split("-")[1]) + 1
                    except Exception:
                        pass
                self.staff_code = f"{prefix}-{str(new_number).zfill(3)}"

        super().save(*args, **kwargs)

        # Sync is_active to Django User
        if self.user_id:
            User.objects.filter(pk=self.user_id).update(is_active=self.is_active)

    def __str__(self):
        return f"{self.staff_code} - {self.user.username}"

    class Meta:
        indexes = [
            models.Index(fields=["staff_code"]),
            models.Index(fields=["role"]),
        ]


# ─────────────────────────────────────────────
# Doctor Profile
# ─────────────────────────────────────────────
class DoctorProfile(models.Model):

    doctor_id = models.AutoField(primary_key=True)
    staff = models.OneToOneField(
        StaffProfile, on_delete=models.CASCADE,
        related_name="doctor_profile", null=True, blank=True
    )
    specialization = models.CharField(max_length=100, default="General")
    consultation_fee = models.PositiveIntegerField(default=500)
    experience_years = models.PositiveIntegerField(default=1)

    def clean(self):
        if self.staff:
            if self.staff.role != "Doctor":
                raise ValidationError("Assigned staff must have role 'Doctor'.")
            # NOTE: Removed is_active check — admin must be able to
            # deactivate a doctor without breaking the profile record.

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{getattr(self.staff, 'staff_code', 'No Staff')} - {self.specialization}"


# ─────────────────────────────────────────────
# Receptionist Profile
# ─────────────────────────────────────────────
class ReceptionistProfile(models.Model):

    profile_id = models.AutoField(primary_key=True)
    staff = models.OneToOneField(
        StaffProfile, on_delete=models.CASCADE,
        related_name="receptionist_profile", null=True, blank=True
    )

    def clean(self):
        if self.staff and self.staff.role != "Receptionist":
            raise ValidationError("Assigned staff must have role 'Receptionist'.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{getattr(self.staff, 'staff_code', 'No Staff')} - Receptionist"


# ─────────────────────────────────────────────
# Lab Technician Profile
# ─────────────────────────────────────────────
class LabTechnicianProfile(models.Model):

    profile_id = models.AutoField(primary_key=True)
    staff = models.OneToOneField(
        StaffProfile, on_delete=models.CASCADE,
        related_name="labtech_profile", null=True, blank=True
    )
    certification_details = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Optional additional certification"
    )

    def clean(self):
        if self.staff and self.staff.role != "Lab Technician":
            raise ValidationError("Assigned staff must have role 'Lab Technician'.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{getattr(self.staff, 'staff_code', 'No Staff')} - Lab Technician"


# ─────────────────────────────────────────────
# Pharmacist Profile
# ─────────────────────────────────────────────
class PharmacistProfile(models.Model):

    staff = models.OneToOneField(
        StaffProfile, on_delete=models.CASCADE,
        related_name="pharmacist_profile", null=True, blank=True
    )
    license_number = models.CharField(max_length=100, blank=True, null=True)
    def clean(self):
        if self.staff and self.staff.role != "Pharmacist":
            raise ValidationError("Assigned staff must have role 'Pharmacist'.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{getattr(self.staff, 'staff_code', 'No Staff')} - Pharmacist"


# ─────────────────────────────────────────────
# Audit Log
# ─────────────────────────────────────────────
class AuditLog(models.Model):

    ACTION_CHOICES = [
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("REACTIVATE", "Reactivate"),
    ]

    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    module = models.CharField(max_length=50, default="General")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    object_id = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.module}"
