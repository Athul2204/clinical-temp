from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import (
    StaffProfile,
    DoctorProfile,
    ReceptionistProfile,
    LabTechnicianProfile,
    PharmacistProfile,
    AuditLog
)
from .serializers import (
    StaffProfileSerializer,
    DoctorProfileSerializer,
    ReceptionistProfileSerializer,
    LabTechnicianProfileSerializer,
    PharmacistProfileSerializer,
    AuditLogSerializer
)

# ------------------------------
# Staff ViewSet
# ------------------------------
class StaffProfileViewSet(viewsets.ModelViewSet):
    queryset = StaffProfile.objects.all()
    serializer_class = StaffProfileSerializer

# ------------------------------
# Doctor ViewSet
# ------------------------------
class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer

# ------------------------------
# Receptionist ViewSet
# ------------------------------
class ReceptionistProfileViewSet(viewsets.ModelViewSet):
    queryset = ReceptionistProfile.objects.all()
    serializer_class = ReceptionistProfileSerializer

# ------------------------------
# Lab Technician ViewSet
# ------------------------------
class LabTechnicianProfileViewSet(viewsets.ModelViewSet):
    queryset = LabTechnicianProfile.objects.all()
    serializer_class = LabTechnicianProfileSerializer

# ------------------------------
# Pharmacist ViewSet
# ------------------------------
class PharmacistProfileViewSet(viewsets.ModelViewSet):
    queryset = PharmacistProfile.objects.all()
    serializer_class = PharmacistProfileSerializer

# ------------------------------
# Audit Log ViewSet (Read Only)
# ------------------------------
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer