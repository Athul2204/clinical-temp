from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import LabTest, LabOrder, LabOrderItem, LabResult, LabBill, LabEquipment, LabMaintenance
from .serializers import LabTestSerializer, LabOrderSerializer, LabOrderItemSerializer, LabResultSerializer, LabBillSerializer, LabEquipmentSerializer, LabMaintenanceSerializer

class LabTestViewSet(viewsets.ModelViewSet):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer
    permission_classes = [IsAuthenticated]

class LabOrderViewSet(viewsets.ModelViewSet):
    queryset = LabOrder.objects.all()
    serializer_class = LabOrderSerializer
    permission_classes = [IsAuthenticated]

class LabOrderItemViewSet(viewsets.ModelViewSet):
    queryset = LabOrderItem.objects.all()
    serializer_class = LabOrderItemSerializer
    permission_classes = [IsAuthenticated]

class LabResultViewSet(viewsets.ModelViewSet):
    queryset = LabResult.objects.all()
    serializer_class = LabResultSerializer
    permission_classes = [IsAuthenticated]

class LabBillViewSet(viewsets.ModelViewSet):
    queryset = LabBill.objects.all()
    serializer_class = LabBillSerializer
    permission_classes = [IsAuthenticated]

class LabEquipmentViewSet(viewsets.ModelViewSet):
    queryset = LabEquipment.objects.all()
    serializer_class = LabEquipmentSerializer
    permission_classes = [IsAuthenticated]

class LabMaintenanceViewSet(viewsets.ModelViewSet):
    queryset = LabMaintenance.objects.all()
    serializer_class = LabMaintenanceSerializer
    permission_classes = [IsAuthenticated]