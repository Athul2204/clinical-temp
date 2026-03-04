# cmsbackend/pharmacist/views.py
from rest_framework import viewsets
from .models import Medicine, MedicineBatch, Dispense, DispenseItem, MedicineBill
from .serializers import MedicineSerializer, MedicineBatchSerializer, DispenseSerializer, DispenseItemSerializer, MedicineBillSerializer

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

class MedicineBatchViewSet(viewsets.ModelViewSet):
    queryset = MedicineBatch.objects.all()
    serializer_class = MedicineBatchSerializer

class DispenseViewSet(viewsets.ModelViewSet):
    queryset = Dispense.objects.all()
    serializer_class = DispenseSerializer

class DispenseItemViewSet(viewsets.ModelViewSet):
    queryset = DispenseItem.objects.all()
    serializer_class = DispenseItemSerializer

class MedicineBillViewSet(viewsets.ModelViewSet):
    queryset = MedicineBill.objects.all()
    serializer_class = MedicineBillSerializer