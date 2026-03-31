
# from django.db import models
# from django.utils import timezone
# from django.core.validators import MinValueValidator
# from django.core.exceptions import ValidationError
# from administration.models import DoctorProfile

# from datetime import date


# # ------------------------------
# # DOB VALIDATION (IMPORTANT FIX)
# # ------------------------------
# def validate_dob(value):
#     if value > date.today():
#         raise ValidationError("Date of birth cannot be in the future")


# # ------------------------------
# # Patient Table
# # ------------------------------
# class Patient(models.Model):

#     patient_id = models.AutoField(primary_key=True)

#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)

#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=15)


    
#     date_of_birth = models.DateField(validators=[validate_dob])

#     age = models.PositiveIntegerField(blank=True, null=True, editable=False)

#     gender_choices = [
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#         ('Other', 'Other')
#     ]
#     gender = models.CharField(max_length=10, choices=gender_choices)

#     # Blood Group Choices
#     blood_group_choices = [
#         ('A+', 'A+'),
#         ('A-', 'A-'),
#         ('B+', 'B+'),
#         ('B-', 'B-'),
#         ('AB+', 'AB+'),
#         ('AB-', 'AB-'),
#         ('O+', 'O+'),
#         ('O-', 'O-'),
#     ]

#     blood_group = models.CharField(
#         max_length=3,
#         choices=blood_group_choices,
#         blank=True,
#         null=True
#     )

#     address = models.TextField()

#     membership_status_choices = [
#         ('Regular', 'Regular'),
#         ('Premium', 'Premium')
#     ]

#     membership_status = models.CharField(
#         max_length=20,
#         choices=membership_status_choices,
#         default='Regular'
#     )

#     created_at = models.DateTimeField(default=timezone.now, editable=False)

#     def save(self, *args, **kwargs):
#         today = timezone.now().date()

#         self.age = (
#             today.year
#             - self.date_of_birth.year
#             - ((today.month, today.day) <
#                (self.date_of_birth.month, self.date_of_birth.day))
#         )

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"


# # ------------------------------
# # Doctor Availability
# # ------------------------------
# class DoctorAvailability(models.Model):

#     availability_id = models.AutoField(primary_key=True)

#     doctor = models.ForeignKey(
#         DoctorProfile,
#         on_delete=models.CASCADE
#     )

#     available_date = models.DateField()

#     start_time = models.TimeField()
#     end_time = models.TimeField()

#     class Meta:
#         unique_together = (
#             'doctor',
#             'available_date',
#             'start_time',
#             'end_time'
#         )

#     def clean(self):
#         if self.start_time and self.end_time:   # ✅ check first
#          if self.start_time >= self.end_time:
#             raise ValidationError("End time must be after start time")
        
#     def __str__(self):
#         return f"{self.doctor} on {self.available_date}"


# # ------------------------------
# # Appointment
# # ------------------------------
# class Appointment(models.Model):

#     appointment_id = models.AutoField(primary_key=True)

#     patient = models.ForeignKey(
#         Patient,
#         on_delete=models.CASCADE,
#         related_name="appointments"
#     )

#     doctor = models.ForeignKey(
#         DoctorProfile,
#         on_delete=models.CASCADE,
#         related_name="appointments"
#     )

#     appointment_date = models.DateField()

#     appointment_time = models.TimeField()

#     token_number = models.PositiveIntegerField(
#         validators=[MinValueValidator(1)]
#     )

#     reason = models.TextField()

#     status_choices = [
#         ('Scheduled', 'Scheduled'),
#         ('Completed', 'Completed'),
#         ('Cancelled', 'Cancelled')
#     ]

#     status = models.CharField(
#         max_length=20,
#         choices=status_choices,
#         default='Scheduled'
#     )

#     created_at = models.DateTimeField(
#         default=timezone.now,
#         editable=False
#     )

#     class Meta:
#         unique_together = (
#             ('doctor', 'appointment_date', 'appointment_time'),
#             ('doctor', 'appointment_date', 'token_number'),
#         )

#     def clean(self):

#         if self.appointment_date < timezone.now().date():
#             raise ValidationError("Appointment date cannot be in the past")

#         if (
#             self.appointment_date == timezone.now().date()
#             and self.appointment_time < timezone.now().time()
#         ):
#             raise ValidationError("Appointment time cannot be in the past")

#     def __str__(self):
#         return f"{self.patient} with {self.doctor}"


# # ------------------------------
# # Consultation Bill
# # ------------------------------
# class ConsultationBill(models.Model):

#     bill_id = models.AutoField(primary_key=True)

#     appointment = models.OneToOneField(
#         Appointment,
#         on_delete=models.CASCADE
#     )

#     amount = models.PositiveIntegerField(
#         validators=[MinValueValidator(0)]
#     )

#     status_choices = [
#         ('Paid', 'Paid'),
#         ('Unpaid', 'Unpaid')
#     ]

#     status = models.CharField(
#         max_length=20,
#         choices=status_choices,
#         default='Unpaid'
#     )

#     created_at = models.DateTimeField(
#         default=timezone.now,
#         editable=False
#     )

#     def __str__(self):
#         return f"Bill {self.bill_id}"
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from administration.models import DoctorProfile
from datetime import date, datetime, timedelta


# ------------------------------
# DOB VALIDATION
# ------------------------------
def validate_dob(value):
    if value > date.today():
        raise ValidationError("Date of birth cannot be in the future")


# ------------------------------
# Patient Table
# ------------------------------
class Patient(models.Model):

    patient_id = models.AutoField(primary_key=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    date_of_birth = models.DateField(validators=[validate_dob])
    age = models.PositiveIntegerField(blank=True, null=True, editable=False)

    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    gender = models.CharField(max_length=10, choices=gender_choices)

    blood_group_choices = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    blood_group = models.CharField(
        max_length=3,
        choices=blood_group_choices,
        blank=True,
        null=True
    )

    address = models.TextField()

    membership_status_choices = [
        ('Regular', 'Regular'),
        ('Premium', 'Premium')
    ]

    membership_status = models.CharField(
        max_length=20,
        choices=membership_status_choices,
        default='Regular'
    )

    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        today = timezone.now().date()
        self.age = (
            today.year - self.date_of_birth.year
            - ((today.month, today.day) <
               (self.date_of_birth.month, self.date_of_birth.day))
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ------------------------------
# Doctor Availability
# ------------------------------
class DoctorAvailability(models.Model):

    availability_id = models.AutoField(primary_key=True)

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE
    )

    available_date = models.DateField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = (
            'doctor',
            'available_date',
            'start_time',
            'end_time'
        )

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")

    def __str__(self):
        return f"{self.doctor}"


# ------------------------------
# Appointment
# ------------------------------
class Appointment(models.Model):

    appointment_id = models.AutoField(primary_key=True)

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    token_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        blank=True,
        null=True
    )

    manual_token = models.BooleanField(default=False)

    reason = models.TextField()

    consultation_fee = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        editable=False,
        null=True,
        blank=True
    )

    status_choices = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ]

    status = models.CharField(
        max_length=20,
        choices=status_choices,
        default='Scheduled'
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False
    )

    class Meta:
        unique_together = (
            ('doctor', 'appointment_date', 'token_number'),
        )

    # ------------------------------
    # VALIDATION
    # ------------------------------
    def clean(self):

        if not self.doctor:
            raise ValidationError("Doctor is required")

        if self.doctor.staff and not self.doctor.staff.is_active:
            raise ValidationError("Cannot book inactive doctor")

        now = timezone.now()

        if self.appointment_date < now.date():
            raise ValidationError("Appointment date cannot be in the past")

        if self.appointment_date == now.date():
            appointment_datetime = timezone.make_aware(
                datetime.combine(self.appointment_date, self.appointment_time)
            )
            if appointment_datetime < now - timedelta(minutes=2):
                raise ValidationError("Appointment time cannot be in the past")

    # ------------------------------
    # SAVE LOGIC  ✅ FIX: removed self.full_clean()
    # full_clean() inside save() causes uncaught Django ValidationError
    # which DRF serializer cannot catch → silent 500 crash on frontend
    # ------------------------------
    def save(self, *args, **kwargs):

        # Auto token (only if not manual)
        if not self.manual_token:
            last_token = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=self.appointment_date
            ).exclude(
                pk=self.pk  # ✅ exclude self when updating
            ).aggregate(models.Max('token_number'))['token_number__max']

            self.token_number = (last_token or 0) + 1

        # Store consultation fee
        if self.doctor:
            self.consultation_fee = self.doctor.consultation_fee or 0  # ✅ FIX: fallback to 0

        # ✅ FIX: REMOVED self.full_clean() — was causing uncaught ValidationError
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient} | Token {self.token_number} | {self.doctor}"


# ------------------------------
# Consultation Bill
# ------------------------------
class ConsultationBill(models.Model):

    bill_id = models.AutoField(primary_key=True)

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="bill"
    )

    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        editable=False
    )

    status_choices = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid')
    ]

    status = models.CharField(
        max_length=20,
        choices=status_choices,
        default='Unpaid'
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False
    )

    # ✅ FIX: fallback to 0 if consultation_fee is None
    def save(self, *args, **kwargs):
        if self.appointment:
            self.amount = self.appointment.consultation_fee or 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill {self.bill_id} - ₹{self.amount}"


# ------------------------------
# AUTO CREATE BILL (signal)
# ------------------------------
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Appointment)
def create_bill(sender, instance, created, **kwargs):
    if created:
        ConsultationBill.objects.create(appointment=instance)