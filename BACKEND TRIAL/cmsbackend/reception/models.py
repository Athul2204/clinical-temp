from django.db import models
from administration.models import User, DoctorProfile


# =========================
# PATIENT MODEL
# =========================

class Patient(models.Model):
    patient_code = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    membership_status = models.CharField(
        max_length=50,
        default="Regular"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_code} - {self.first_name}"


# =========================
# DOCTOR AVAILABILITY
# =========================

class DoctorAvailability(models.Model):
    DAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name="availabilities"
    )
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor} - {self.get_day_of_week_display()}"


# =========================
# APPOINTMENT
# =========================

class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    appointment_code = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        related_name="appointments"
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    token_number = models.PositiveIntegerField(null=True, blank=True)
    reason = models.TextField(blank=True)
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Scheduled"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_appointments"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.appointment_code


# =========================
# CONSULTATION BILL
# =========================

class ConsultationBill(models.Model):
    bill_code = models.CharField(max_length=20, unique=True)
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="consultation_bill"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=30)
    payment_mode = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bill_code