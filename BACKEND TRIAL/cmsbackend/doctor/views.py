from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Consultation, Prescription, PrescriptionItem, LabTestRequest, LabTestRequestItem
from .serializers import ConsultationSerializer, PrescriptionSerializer, PrescriptionItemSerializer, LabTestRequestSerializer, LabTestRequestItemSerializer

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated]

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

class PrescriptionItemViewSet(viewsets.ModelViewSet):
    queryset = PrescriptionItem.objects.all()
    serializer_class = PrescriptionItemSerializer
    permission_classes = [IsAuthenticated]

class LabTestRequestViewSet(viewsets.ModelViewSet):
    queryset = LabTestRequest.objects.all()
    serializer_class = LabTestRequestSerializer
    permission_classes = [IsAuthenticated]

class LabTestRequestItemViewSet(viewsets.ModelViewSet):
    queryset = LabTestRequestItem.objects.all()
    serializer_class = LabTestRequestItemSerializer
    permission_classes = [IsAuthenticated]