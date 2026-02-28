from django.db import models
from administration.models import DoctorProfile
from reception.models import Appointment


class Consultation(models.Model):
    consultation_code = models.CharField(max_length=20, unique=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    vitals = models.TextField()
    advice = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Prescription(models.Model):
    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Sent", "Sent"),
        ("Dispensed", "Dispensed"),
    ]

    prescription_code = models.CharField(max_length=20, unique=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=150)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration = models.PositiveIntegerField()
    instructions = models.TextField(blank=True)


class LabTestRequest(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)