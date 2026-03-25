from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Patient, DoctorAvailability, Appointment, ConsultationBill
from .serializers import (
    PatientSerializer,
    DoctorAvailabilitySerializer,
    AppointmentSerializer,
    ConsultationBillSerializer,
)


# -----------------------------
# Patient ViewSet
# -----------------------------
class PatientViewSet(viewsets.ModelViewSet):

    queryset = Patient.objects.all().order_by("first_name")
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]


# -----------------------------
# Doctor Availability ViewSet
# -----------------------------
class DoctorAvailabilityViewSet(viewsets.ModelViewSet):

    queryset = DoctorAvailability.objects.all().order_by("available_date")
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [IsAuthenticated]


# -----------------------------
# Appointment ViewSet
# -----------------------------
class AppointmentViewSet(viewsets.ModelViewSet):

    queryset = Appointment.objects.all().order_by(
        "appointment_date",
        "token_number"
    )

    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        Appointment = serializer.save()

        ConsultationBill.objects.create(
            appointment=Appointment,
            patient=Appointment,
            amount=Appointment.doctor.consultation_fee
        )


# -----------------------------
# Consultation Bill ViewSet
# -----------------------------
class ConsultationBillViewSet(viewsets.ModelViewSet):

    queryset = ConsultationBill.objects.all().order_by("-created_at")
    serializer_class = ConsultationBillSerializer
    permission_classes = [IsAuthenticated]



    