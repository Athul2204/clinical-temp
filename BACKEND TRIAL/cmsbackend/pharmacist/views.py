
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import MedicineSerializer, MedicineBatchSerializer, DispenseSerializer, DispenseItemSerializer, MedicineBillSerializer,MedicineStockLogSerializer
from doctor.models import Prescription
from .models import Medicine, MedicineBatch, Dispense, DispenseItem, MedicineBill,MedicineStockLog
from .serializers import IncomingPrescriptionSerializer
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsPharmacist
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class MedicineViewSet(ModelViewSet):

    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']  
    permission_classes = [IsAuthenticated,IsPharmacist]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Medicine added successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Medicine updated successfully",
                "data": serializer.data
            }
        )

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.delete()

        return Response(
            {"message": "Medicine deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

# class MedicineBatchViewSet(viewsets.ModelViewSet):
#     queryset = MedicineBatch.objects.all()
#     serializer_class = MedicineBatchSerializer
class MedicineBatchViewSet(ModelViewSet):

    queryset = MedicineBatch.objects.all()
    serializer_class = MedicineBatchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['medicine'] 
    permission_classes = [IsAuthenticated,IsPharmacist]
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Medicine batch added successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

# class DispenseViewSet(viewsets.ModelViewSet):
#     queryset = Dispense.objects.all()
#     serializer_class = DispenseSerializer

# class DispenseItemViewSet(viewsets.ModelViewSet):
#     queryset = DispenseItem.objects.all()
#     serializer_class = DispenseItemSerializer
class DispenseViewSet(ModelViewSet):

    queryset = Dispense.objects.all()
    serializer_class = DispenseSerializer
    permission_classes = [IsAuthenticated,IsPharmacist]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['prescription', 'status']
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dispense = serializer.save()

        return Response(
            {
                "message": "Medicine dispensed successfully",
                "data": DispenseSerializer(dispense).data
            },
            status=status.HTTP_201_CREATED
        )
class DispenseItemViewSet(ReadOnlyModelViewSet):
    queryset = DispenseItem.objects.all()
    serializer_class = DispenseItemSerializer
    permission_classes = [IsAuthenticated,IsPharmacist]

class MedicineStockLogViewSet(ReadOnlyModelViewSet):
    queryset = MedicineStockLog.objects.all()
    serializer_class = MedicineStockLogSerializer
    permission_classes = [IsAuthenticated,IsPharmacist]

# class MedicineBillViewSet(viewsets.ModelViewSet):
#     queryset = MedicineBill.objects.all()
#     serializer_class = MedicineBillSerializer
class MedicineBillViewSet(ModelViewSet):

    queryset = MedicineBill.objects.all()
    serializer_class = MedicineBillSerializer
    permission_classes = [IsAuthenticated,IsPharmacist]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Medicine bill created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class SentPrescriptionListView(APIView):
    permission_classes = [IsAuthenticated, IsPharmacist]

    def get(self, request):
        prescriptions = Prescription.objects.filter(
            status="Sent"
        ).select_related(
            'consultation__appointment__patient',
            'doctor'
        ).prefetch_related('items__medicine_name')

        serializer = IncomingPrescriptionSerializer(prescriptions, many=True)
        return Response(
            {
                "message": "Sent prescriptions fetched successfully",
                "count": prescriptions.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class SentPrescriptionDetailView(APIView):
    permission_classes = [IsAuthenticated, IsPharmacist]

    def get(self, request, prescription_code):
        try:
            prescription = Prescription.objects.select_related(
                'consultation__appointment__patient',
                'doctor'
            ).prefetch_related('items__medicine_name').get(
                prescription_code=prescription_code,
                status="Sent"
            )
        except Prescription.DoesNotExist:
            return Response(
                {"message": "Prescription not found or not yet sent"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = IncomingPrescriptionSerializer(prescription)
        return Response(
            {
                "message": "Prescription details fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )