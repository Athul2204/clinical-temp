# from django.db import models
# from django.core.exceptions import ValidationError
# from django.utils import timezone
# from administration.models import DoctorProfile, User


# # =========================
# # PATIENT MODEL
# # =========================

# class Patient(models.Model):

#     patient_code = models.CharField(max_length=20, unique=True, editable=False)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100, blank=True)
#     gender = models.CharField(max_length=10)
#     phone = models.CharField(max_length=15)
#     email = models.EmailField(blank=True)
#     address = models.TextField(blank=True)
#     membership_status = models.CharField(max_length=50, default="Regular")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         if not self.patient_code:
#             last_patient = Patient.objects.order_by("-id").first()
#             if last_patient:
#                 last_number = int(last_patient.patient_code.split("-")[1])
#                 new_number = last_number + 1
#             else:
#                 new_number = 1

#             self.patient_code = f"PAT-{str(new_number).zfill(3)}"

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.patient_code


# # =========================
# # DOCTOR AVAILABILITY
# # =========================

# class DoctorAvailability(models.Model):
#     doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
#     day_of_week = models.IntegerField()  # 0=Monday
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     is_active = models.BooleanField(default=True)

#     def clean(self):
#         if self.start_time >= self.end_time:
#             raise ValidationError("End time must be after start time")


# # =========================
# # APPOINTMENT
# # =========================

# class Appointment(models.Model):

#     STATUS_CHOICES = [
#         ("Scheduled", "Scheduled"),
#         ("Completed", "Completed"),
#         ("Cancelled", "Cancelled"),
#     ]

#     appointment_code = models.CharField(max_length=20, unique=True, editable=False)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     doctor = models.ForeignKey(DoctorProfile, on_delete=models.PROTECT)
#     appointment_date = models.DateField()
#     appointment_time = models.TimeField()
#     token_number = models.PositiveIntegerField(editable=False)
#     status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Scheduled")
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def clean(self):

#         # Prevent past date booking
#         if self.appointment_date < timezone.now().date():
#             raise ValidationError("Cannot book appointment in the past")

#         # Check doctor availability
#         weekday = self.appointment_date.weekday()
#         availability = DoctorAvailability.objects.filter(
#             doctor=self.doctor,
#             day_of_week=weekday,
#             is_active=True,
#             start_time__lte=self.appointment_time,
#             end_time__gte=self.appointment_time
#         ).exists()

#         if not availability:
#             raise ValidationError("Doctor not available at this time")

#         # Prevent double booking
#         conflict = Appointment.objects.filter(
#             doctor=self.doctor,
#             appointment_date=self.appointment_date,
#             appointment_time=self.appointment_time
#         ).exclude(id=self.id).exists()

#         if conflict:
#             raise ValidationError("Doctor already booked at this time")

#     def save(self, *args, **kwargs):

#         if not self.appointment_code:
#             last = Appointment.objects.order_by("-id").first()
#             if last:
#                 last_number = int(last.appointment_code.split("-")[1])
#                 new_number = last_number + 1
#             else:
#                 new_number = 1

#             self.appointment_code = f"APT-{str(new_number).zfill(3)}"

#         # Auto token generation per doctor per day
#         if not self.token_number:
#             last_token = Appointment.objects.filter(
#                 doctor=self.doctor,
#                 appointment_date=self.appointment_date
#             ).order_by("-token_number").first()

#             self.token_number = (last_token.token_number + 1) if last_token else 1

#         self.full_clean()
#         super().save(*args, **kwargs)

#     def cancel(self):
#         if self.status == "Cancelled":
#             raise ValidationError("Appointment already cancelled")

#         if self.appointment_date < timezone.now().date():
#             raise ValidationError("Cannot cancel past appointments")

#         self.status = "Cancelled"
#         self.save()

#     def __str__(self):
#         return self.appointment_code


# # =========================
# # CONSULTATION BILL
# # =========================

# class ConsultationBill(models.Model):

#     PAYMENT_STATUS = [
#         ("Pending", "Pending"),
#         ("Paid", "Paid"),
#     ]

#     bill_code = models.CharField(max_length=20, unique=True, editable=False)
#     appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
#     payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS, default="Pending")
#     payment_mode = models.CharField(max_length=30)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):

#         if not self.bill_code:
#             last = ConsultationBill.objects.order_by("-id").first()
#             if last:
#                 last_number = int(last.bill_code.split("-")[1])
#                 new_number = last_number + 1
#             else:
#                 new_number = 1

#             self.bill_code = f"BILL-{str(new_number).zfill(3)}"

#         # Auto fetch consultation fee
#         self.amount = self.appointment.doctor.consultation_fee

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.bill_code

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from administration.models import DoctorProfile

# ------------------------------
# Patient Table
# ------------------------------
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    age = models.PositiveIntegerField(blank=True, null=True, editable=False)
    gender_choices = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    gender = models.CharField(max_length=10, choices=gender_choices)
    address = models.TextField()
    membership_status_choices = [('Regular', 'Regular'), ('Premium', 'Premium')]
    membership_status = models.CharField(max_length=20, choices=membership_status_choices, default='Regular')
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        # Calculate age from DOB
        today = timezone.now().date()
        self.age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



# Doctor Availability Table
# ------------------------------
class DoctorAvailability(models.Model):
    availability_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    available_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('doctor', 'available_date', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.doctor.staff.user.username} on {self.available_date}"


# ------------------------------
# Appointment Table
# ------------------------------
class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    token_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    reason = models.TextField()
    status_choices = [('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')]
    status = models.CharField(max_length=20, choices=status_choices, default='Scheduled')
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        unique_together = ('doctor', 'appointment_date', 'appointment_time')

    def __str__(self):
        return f"{self.patient.first_name} with Dr.{self.doctor.staff.user.username} on {self.appointment_date}"

# ------------------------------
# Consultation Billing Table
# ------------------------------
class ConsultationBill(models.Model):
    bill_id = models.AutoField(primary_key=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    status_choices = [('Paid', 'Paid'), ('Unpaid', 'Unpaid')]
    status = models.CharField(max_length=20, choices=status_choices, default='Unpaid')
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"Bill {self.bill_id} for {self.appointment}"