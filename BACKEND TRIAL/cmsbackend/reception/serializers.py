from rest_framework import serializers
from .models import (
    Patient, Appointment,
    DoctorAvailability, ConsultationBill
)
from administration.models import DoctorProfile


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=DoctorProfile.objects.all()
    )

    class Meta:
        model = Appointment
        fields = "__all__"


class ConsultationBillSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(read_only=True)

    class Meta:
        model = ConsultationBill
        fields = "__all__"


