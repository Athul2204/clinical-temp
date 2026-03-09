from rest_framework import serializers
from .models import Patient, Appointment, DoctorAvailability, ConsultationBill
from administration.models import DoctorProfile
from django.utils import timezone


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = "__all__"

    def validate_phone(self, value):

        if not value.isdigit():
            raise serializers.ValidationError(
            "Phone number must contain only digits"
        )

        if len(value) != 10:
            raise serializers.ValidationError(
            "Phone number must contain exactly 10 digits"
        )

        return value

    def validate_first_name(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "First name cannot be empty"
            )

        return value


class DoctorAvailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorAvailability
        fields = "__all__"

    def validate(self, data):

        start_time = data.get("start_time")
        end_time = data.get("end_time")
        available_date = data.get("available_date")

        # start time validation
        if start_time >= end_time:
            raise serializers.ValidationError(
                "Start time must be earlier than end time"
            )

        # past date validation
        if available_date < timezone.now().date():
            raise serializers.ValidationError(
                "Availability date cannot be in the past"
            )

        return data

class AppointmentSerializer(serializers.ModelSerializer):

    patient_name = serializers.CharField(
        source="patient.first_name",
        read_only=True
    )

    doctor = serializers.PrimaryKeyRelatedField(
        queryset=DoctorProfile.objects.all()
    )

    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, data):

        doctor = data.get("doctor")
        date = data.get("appointment_date")
        time = data.get("appointment_time")
        token = data.get("token_number")

        # Doctor availability check
        availability = DoctorAvailability.objects.filter(
            doctor=doctor,
            available_date=date,
            start_time__lte=time,
            end_time__gte=time
        ).exists()

        if not availability:
            raise serializers.ValidationError(
                "Doctor is not available at this time"
            )

        # Token duplicate check (safe for update)
        appointment_qs = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=date,
            token_number=token
        )

        if self.instance:
            appointment_qs = appointment_qs.exclude(
                pk=self.instance.pk
            )

        if appointment_qs.exists():
            raise serializers.ValidationError(
                "Token number already exists for this date"
            )

        return data

class ConsultationBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsultationBill
        fields = "__all__"

    def validate_amount(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "Amount cannot be negative"
            )

        return value