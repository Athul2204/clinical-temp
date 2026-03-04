from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Patient, DoctorAvailability, Appointment, ConsultationBill
from .serializers import PatientSerializer, DoctorAvailabilitySerializer, AppointmentSerializer, ConsultationBillSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [IsAuthenticated]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

class ConsultationBillViewSet(viewsets.ModelViewSet):
    queryset = ConsultationBill.objects.all()
    serializer_class = ConsultationBillSerializer
    permission_classes = [IsAuthenticated]