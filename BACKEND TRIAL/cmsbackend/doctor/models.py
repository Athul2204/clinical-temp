from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from administration.models import DoctorProfile
from reception.models import Appointment


# =========================
# CONSULTATION
# =========================

class Consultation(models.Model):

    consultation_code = models.CharField(max_length=20, unique=True, editable=False)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    vitals = models.TextField()
    advice = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):

        # Appointment must be today
        if self.appointment.appointment_date != timezone.now().date():
            raise ValidationError("Consultation allowed only for today's appointment")

        # Prevent consultation for cancelled appointment
        if self.appointment.status == "Cancelled":
            raise ValidationError("Cannot consult cancelled appointment")

    def save(self, *args, **kwargs):

        if not self.consultation_code:
            last = Consultation.objects.order_by("-id").first()
            if last:
                last_number = int(last.consultation_code.split("-")[1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.consultation_code = f"CONS-{str(new_number).zfill(3)}"

        self.full_clean()
        super().save(*args, **kwargs)

        # Auto mark appointment completed
        self.appointment.status = "Completed"
        self.appointment.save()

    def __str__(self):
        return self.consultation_code


# =========================
# PRESCRIPTION
# =========================

class Prescription(models.Model):

    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Sent", "Sent"),
        ("Dispensed", "Dispensed"),
    ]

    prescription_code = models.CharField(max_length=20, unique=True, editable=False)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Draft")
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):

        # Ensure doctor matches consultation appointment doctor
        if self.consultation.appointment.doctor != self.doctor:
            raise ValidationError("Doctor mismatch with appointment")

    def save(self, *args, **kwargs):

        if not self.prescription_code:
            last = Prescription.objects.order_by("-id").first()
            if last:
                last_number = int(last.prescription_code.split("-")[1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.prescription_code = f"PR-{str(new_number).zfill(3)}"

        self.full_clean()
        super().save(*args, **kwargs)

    def send_to_pharmacy(self):
        if not self.items.exists():
            raise ValidationError("Cannot send empty prescription")

        if self.status != "Draft":
            raise ValidationError("Only draft prescriptions can be sent")

        self.status = "Sent"
        self.save()

    def __str__(self):
        return self.prescription_code


# =========================
# PRESCRIPTION ITEM
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
    duration = models.PositiveIntegerField()
    instructions = models.TextField(blank=True)

    def clean(self):
        if self.duration <= 0:
            raise ValidationError("Duration must be positive")


# =========================
# LAB TEST REQUEST
# =========================

class LabTestRequest(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
    ]

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name="lab_requests"
    )
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.consultation.appointment.doctor != self.doctor:
            raise ValidationError("Doctor mismatch with consultation")

    def __str__(self):
        return f"LabRequest-{self.id}"