from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator
from pharmacist.models import Medicine
# =========================
# CONSULTATION
# =========================
class Consultation(models.Model):
    consultation_code = models.CharField(max_length=20, unique=True, editable=False)
    appointment = models.OneToOneField(
        "reception.Appointment", on_delete=models.CASCADE
    )
    symptoms = models.TextField()
    diagnosis = models.TextField()
    vitals = models.TextField()
    advice = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def clean(self):
        # Only allow consultation for today's appointment
        if self.appointment.appointment_date != timezone.now().date():
            raise ValidationError("Consultation allowed only for today's appointment")
        if self.appointment.status == "Cancelled":
            raise ValidationError("Cannot consult cancelled appointment")

    def save(self, *args, **kwargs):
        if not self.consultation_code:
            last = Consultation.objects.order_by("-id").first()
            new_number = 1
            if last:
                try:
                    last_number = int(last.consultation_code.split("-")[1])
                    new_number = last_number + 1
                except:
                    new_number = 1
            self.consultation_code = f"CONS-{str(new_number).zfill(3)}"
        self.full_clean()
        super().save(*args, **kwargs)
        # Update appointment status

    def __str__(self):
        return self.consultation_code


# =========================
# PRESCRIPTION
# =========================
class Prescription(models.Model):
    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Sent", "Sent"),
        ("Dispensed", "Dispensed")
    ]

    prescription_code = models.CharField(max_length=20, unique=True, editable=False)
    consultation = models.OneToOneField(
        Consultation, on_delete=models.CASCADE, related_name="prescription"
    )
    doctor = models.ForeignKey(
        "administration.DoctorProfile", on_delete=models.PROTECT
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Draft")
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    dispensed_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.consultation.appointment.doctor != self.doctor:
            raise ValidationError("Doctor mismatch with appointment")

    def save(self, *args, **kwargs):
        if not self.prescription_code:
            last = Prescription.objects.order_by("-id").first()
            new_number = 1
            if last:
                try:
                    last_number = int(last.prescription_code.split("-")[1])
                    new_number = last_number + 1
                except:
                    new_number = 1
            self.prescription_code = f"PR-{str(new_number).zfill(3)}"
        self.full_clean()
        super().save(*args, **kwargs)

    def send_to_pharmacy(self):

        if not self.items.exists():
            raise ValidationError("Cannot send empty prescription")

        lab_request = getattr(self.consultation, "lab_request", None)
        if lab_request and lab_request.status == "Pending":
            raise ValidationError(
                "Cannot send prescription while lab tests are pending"
            )

        if self.status != "Draft":
            raise ValidationError(
                "Only draft prescriptions can be sent"
            )

        # ✅ Update prescription status
        self.status = "Sent"
        self.sent_at = timezone.now()
        self.save(update_fields=["status", "sent_at"])

        # ✅ NOW mark appointment as Completed
        appointment = self.consultation.appointment
        appointment.status = "Completed"
        appointment.save(update_fields=["status"])

    def __str__(self):
        return self.prescription_code


# =========================
# PRESCRIPTION ITEM
# =========================
class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(
        Prescription, on_delete=models.CASCADE, related_name="items"
    )
    medicine_name = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT
    )
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1)])
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
        ("Completed", "Completed")
    ]
    consultation = models.OneToOneField(
        Consultation, on_delete=models.CASCADE, related_name="lab_request"
    )
    doctor = models.ForeignKey(
        "administration.DoctorProfile", on_delete=models.PROTECT
    )
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.consultation.appointment.doctor != self.doctor:
            raise ValidationError("Doctor mismatch with consultation")

    def __str__(self):
        return f"LabRequest-{self.id}"


# =========================
# LAB TEST REQUEST ITEMS
# =========================
class LabTestRequestItem(models.Model):
    lab_request = models.ForeignKey(
        LabTestRequest, on_delete=models.CASCADE, related_name="tests"
    )
    lab_test = models.ForeignKey(
        "labtechnician.LabTest", on_delete=models.PROTECT
    )

    def clean(self):
        if not self.lab_test:
            raise ValidationError("Lab Test must be selected")

    def __str__(self):
        return f"{self.lab_test.test_name}"
