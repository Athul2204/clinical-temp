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
from django.core.validators import MinValueValidator, RegexValidator, EmailValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# ------------------------------
# Role Table
# ------------------------------
class Role(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        ('Receptionist', 'Receptionist'),
        ('LabTech', 'Lab Technician'),
        ('Pharmacist', 'Pharmacist')
    ]
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

# ------------------------------
# Custom User Table
# ------------------------------
class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return f"{self.username} ({self.role.name})"

# ------------------------------
# Staff Profile Table
# ------------------------------
class StaffProfile(models.Model):
    staff_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, validators=[
        RegexValidator(r'^\+?\d{9,15}$', 'Enter a valid phone number')
    ])
    address = models.TextField(blank=True, null=True)
    salary = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    joining_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} Profile"

# ------------------------------
# Doctor Profile
# ------------------------------
class DoctorProfile(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    consultation_fee = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    experience_years = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Dr. {self.user.username} ({self.specialization})"

# ------------------------------
# Receptionist Profile
# ------------------------------
class ReceptionistProfile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Receptionist: {self.user.username}"

# ------------------------------
# Lab Technician Profile
# ------------------------------
class LabTechnicianProfile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    certification = models.CharField(max_length=255)

    def __str__(self):
        return f"LabTech: {self.user.username}"

# ------------------------------
# Pharmacist Profile
# ------------------------------
class PharmacistProfile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Pharmacist: {self.user.username}"

# ------------------------------
# Audit Log Table
# ------------------------------
class AuditLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"