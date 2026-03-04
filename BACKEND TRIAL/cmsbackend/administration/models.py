# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.core.exceptions import ValidationError
# from django.utils import timezone
# from datetime import date


# # =========================
# # ROLE MODEL
# # =========================

# class Role(models.Model):
#     ROLE_CHOICES = [
#         ("ADMIN", "Admin"),
#         ("DOCTOR", "Doctor"),
#         ("RECEPTIONIST", "Receptionist"),
#         ("LAB_TECH", "Lab Technician"),
#         ("PHARMACIST", "Pharmacist"),
#     ]

#     rolename = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
#     description = models.TextField(blank=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.rolename


# # =========================
# # CUSTOM USER
# # =========================

# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.username


# # =========================
# # STAFF PROFILE
# # =========================

# class StaffProfile(models.Model):

#     ROLE_PREFIX = {
#         "DOCTOR": "DOC",
#         "RECEPTIONIST": "REC",
#         "LAB_TECH": "LAB",
#         "PHARMACIST": "PHM",
#     }

#     MINIMUM_AGE = {
#         "DOCTOR": 24,
#         "RECEPTIONIST": 21,
#         "LAB_TECH": 23,
#         "PHARMACIST": 23,
#     }

#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile")
#     staff_code = models.CharField(max_length=20, unique=True, editable=False)
#     phone = models.CharField(max_length=15)
#     date_of_birth = models.DateField()
#     salary = models.DecimalField(max_digits=10, decimal_places=2)
#     joined_date = models.DateField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)

#     def calculate_age(self):
#         today = date.today()
#         return today.year - self.date_of_birth.year - (
#             (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
#         )

#     def clean(self):
#         role_name = self.user.role.rolename

#         # Salary validation
#         if self.salary <= 0:
#             raise ValidationError("Salary must be greater than 0")

#         # Age validation
#         age = self.calculate_age()
#         minimum_age = self.MINIMUM_AGE.get(role_name)

#         if minimum_age and age < minimum_age:
#             raise ValidationError(
#                 f"{role_name} must be at least {minimum_age} years old"
#             )

#     def save(self, *args, **kwargs):
#         if not self.staff_code:
#             role_name = self.user.role.rolename
#             prefix = self.ROLE_PREFIX.get(role_name)

#             last_staff = StaffProfile.objects.filter(
#                 staff_code__startswith=prefix
#             ).order_by("-id").first()

#             if last_staff:
#                 last_number = int(last_staff.staff_code.split("-")[1])
#                 new_number = last_number + 1
#             else:
#                 new_number = 1

#             self.staff_code = f"{prefix}-{str(new_number).zfill(3)}"

#         self.full_clean()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.staff_code


# # =========================
# # ROLE PROFILES
# # =========================

# class DoctorProfile(models.Model):
#     staff_profile = models.OneToOneField(StaffProfile, on_delete=models.CASCADE)
#     qualification = models.CharField(max_length=150)
#     certifications = models.CharField(max_length=150)
#     specialization = models.CharField(max_length=150)
#     experience_years = models.PositiveIntegerField()
#     consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)

#     def clean(self):
#         if self.consultation_fee <= 0:
#             raise ValidationError("Consultation fee must be positive")


# class ReceptionistProfile(models.Model):
#     staff_profile = models.OneToOneField(StaffProfile, on_delete=models.CASCADE)
#     qualification = models.CharField(max_length=150)
#     shift = models.CharField(max_length=50)


# class LabTechnicianProfile(models.Model):
#     staff_profile = models.OneToOneField(StaffProfile, on_delete=models.CASCADE)
#     qualification = models.CharField(max_length=150)
#     certifications = models.CharField(max_length=150)
#     lab_specialization = models.CharField(max_length=150)


# class PharmacistProfile(models.Model):
#     staff_profile = models.OneToOneField(StaffProfile, on_delete=models.CASCADE)
#     qualification = models.CharField(max_length=150)
#     license_number = models.CharField(max_length=100, unique=True)
#     certifications = models.CharField(max_length=150)


# # =========================
# # AUDIT LOG
# # =========================

# class AuditLog(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     module_name = models.CharField(max_length=100)
#     action_type = models.CharField(max_length=100)
#     record_id = models.IntegerField()
#     timestamp = models.DateTimeField(auto_now_add=True)


from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User


class StaffProfile(models.Model):

    ROLE_CHOICES = [
        ("Doctor", "Doctor"),
        ("Receptionist", "Receptionist"),
        ("Lab Technician", "Lab Technician"),
        ("Pharmacist", "Pharmacist"),
    ]

    id = models.AutoField(primary_key=True)

    staff_code = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        db_index=True
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staff_profile"
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(r'^\+?\d{9,15}$')]
    )

    date_of_birth = models.DateField(null=True, blank=True)

    address = models.TextField(blank=True, null=True)

    qualification = models.CharField(max_length=255)

    salary = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    joining_date = models.DateField(default=timezone.now)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
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

            last_staff = StaffProfile.objects.filter(
                staff_code__startswith=prefix
            ).order_by("-id").first()

            if last_staff:
                last_number = int(last_staff.staff_code.split("-")[1])
                new_number = last_number + 1
            else:
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
        related_name="doctor_profile"
    )

    specialization = models.CharField(max_length=100)

    consultation_fee = models.PositiveIntegerField()

    experience_years = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.staff.staff_code} - {self.specialization}"


# ------------------------------
# Receptionist Profile
# ------------------------------
class ReceptionistProfile(models.Model):

    profile_id = models.AutoField(primary_key=True)

    staff = models.OneToOneField(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="receptionist_profile"
    )

    def __str__(self):
        return f"{self.staff.staff_code} - Receptionist"


# ------------------------------
# Lab Technician Profile
# ------------------------------
class LabTechnicianProfile(models.Model):

    profile_id = models.AutoField(primary_key=True)

    staff = models.OneToOneField(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="labtech_profile"
    )

    certification_details = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Optional additional certification"
    )

    def __str__(self):
        return f"{self.staff.staff_code} - Lab Technician"


# ------------------------------
# Pharmacist Profile
# ------------------------------
class PharmacistProfile(models.Model):

    staff = models.OneToOneField(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="pharmacist_profile"
    )

    license_number = models.CharField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return f"{self.staff.staff_code} - Pharmacist"


# ------------------------------
# Audit Log (Centralized Monitoring)
# ------------------------------from django.db import models
from django.db import models
from django.contrib.auth.models import User

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
    module = models.CharField(max_length=100)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    object_id = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.action} - {self.module}"