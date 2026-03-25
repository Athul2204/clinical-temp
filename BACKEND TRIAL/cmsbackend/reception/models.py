
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
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

    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    gender = models.CharField(max_length=10, choices=gender_choices)

    # Blood Group Choices
    blood_group_choices = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
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
            today.year
            - self.date_of_birth.year
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
            raise ValidationError(
                "Start time must be earlier than end time"
            )

    def __str__(self):
        return f"{self.doctor} on {self.available_date}"


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
        validators=[MinValueValidator(1)]
    )

    reason = models.TextField()

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
            ('doctor', 'appointment_date', 'appointment_time'),
            ('doctor', 'appointment_date', 'token_number'),
        )

    def clean(self):

        if self.appointment_date < timezone.now().date():
            raise ValidationError("Appointment date cannot be in the past")

        if (
            self.appointment_date == timezone.now().date()
            and self.appointment_time < timezone.now().time()
        ):
            raise ValidationError("Appointment time cannot be in the past")

    def __str__(self):
        return f"{self.patient} with {self.doctor}"


# ------------------------------
# Consultation Bill
# ------------------------------
class ConsultationBill(models.Model):

    bill_id = models.AutoField(primary_key=True)

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE
    )

    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
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

    def __str__(self):
        return f"Bill {self.bill_id}"