from django.db import models
from administration.models import DoctorProfile
from reception.models import Appointment


# =========================
# CONSULTATION
# =========================

class Consultation(models.Model):
    consultation_code = models.CharField(max_length=20, unique=True)
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="consultation"
    )
    symptoms = models.TextField()
    observations = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    vitals = models.TextField(blank=True)
    advice = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.consultation_code


# =========================
# PRESCRIPTION
# =========================

class Prescription(models.Model):
    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Final", "Final"),
    ]

    prescription_code = models.CharField(max_length=20, unique=True)
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        related_name="prescriptions"
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Draft"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prescription_code


# =========================
# PRESCRIPTION ITEMS
# =========================

class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name="items"
    )
    medicine_name = models.CharField(max_length=150)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration = models.PositiveIntegerField(help_text="Duration in days")
    instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.medicine_name} ({self.dosage})"