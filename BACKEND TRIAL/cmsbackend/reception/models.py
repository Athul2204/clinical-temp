from django.db import models
from administration.models import DoctorProfile, User


class Patient(models.Model):
    patient_code = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    membership_status = models.CharField(max_length=50, default="Regular")
    created_at = models.DateTimeField(auto_now_add=True)


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    day_of_week = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)


class Appointment(models.Model):
    appointment_code = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.PROTECT)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    token_number = models.PositiveIntegerField()
    status = models.CharField(max_length=30, default="Scheduled")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ConsultationBill(models.Model):
    bill_code = models.CharField(max_length=20, unique=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=30)
    payment_mode = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)