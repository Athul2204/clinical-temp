
# from rest_framework import viewsets
# from rest_framework.views import APIView
# from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import MedicineSerializer, MedicineBatchSerializer, DispenseSerializer, DispenseItemSerializer, MedicineBillSerializer,MedicineStockLogSerializer
# from doctor.models import Prescription
# from .models import Medicine, MedicineBatch, Dispense, DispenseItem, MedicineBill,MedicineStockLog
# from .serializers import IncomingPrescriptionSerializer
# from rest_framework.permissions import IsAuthenticated
# from authentication.permissions import IsPharmacist
# from rest_framework.filters import SearchFilter
# from django_filters.rest_framework import DjangoFilterBackend


# class MedicineViewSet(ModelViewSet):

#     queryset = Medicine.objects.all()
#     serializer_class = MedicineSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['name']  
#     permission_classes = [IsAuthenticated,IsPharmacist]

#     def create(self, request, *args, **kwargs):

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(
#             {
#                 "message": "Medicine added successfully",
#                 "data": serializer.data
#             },
#             status=status.HTTP_201_CREATED
#         )

#     def update(self, request, *args, **kwargs):

#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(
#             {
#                 "message": "Medicine updated successfully",
#                 "data": serializer.data
#             }
#         )

#     def destroy(self, request, *args, **kwargs):

#         instance = self.get_object()
#         instance.delete()

#         return Response(
#             {"message": "Medicine deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT
#         )

# # class MedicineBatchViewSet(viewsets.ModelViewSet):
# #     queryset = MedicineBatch.objects.all()
# #     serializer_class = MedicineBatchSerializer
# class MedicineBatchViewSet(ModelViewSet):

#     queryset = MedicineBatch.objects.all()
#     serializer_class = MedicineBatchSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['medicine'] 
#     permission_classes = [IsAuthenticated,IsPharmacist]
#     def create(self, request, *args, **kwargs):

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(
#             {
#                 "message": "Medicine batch added successfully",
#                 "data": serializer.data
#             },
#             status=status.HTTP_201_CREATED
#         )

# # class DispenseViewSet(viewsets.ModelViewSet):
# #     queryset = Dispense.objects.all()
# #     serializer_class = DispenseSerializer

# # class DispenseItemViewSet(viewsets.ModelViewSet):
# #     queryset = DispenseItem.objects.all()
# #     serializer_class = DispenseItemSerializer
# class DispenseViewSet(ModelViewSet):

#     queryset = Dispense.objects.all()
#     serializer_class = DispenseSerializer
#     permission_classes = [IsAuthenticated,IsPharmacist]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['prescription', 'status']
#     def create(self, request, *args, **kwargs):

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         dispense = serializer.save()

#         return Response(
#             {
#                 "message": "Medicine dispensed successfully",
#                 "data": DispenseSerializer(dispense).data
#             },
#             status=status.HTTP_201_CREATED
#         )
# class DispenseItemViewSet(ReadOnlyModelViewSet):
#     queryset = DispenseItem.objects.all()
#     serializer_class = DispenseItemSerializer
#     permission_classes = [IsAuthenticated,IsPharmacist]

# class MedicineStockLogViewSet(ReadOnlyModelViewSet):
#     queryset = MedicineStockLog.objects.all()
#     serializer_class = MedicineStockLogSerializer
#     permission_classes = [IsAuthenticated,IsPharmacist]

# # class MedicineBillViewSet(viewsets.ModelViewSet):
# #     queryset = MedicineBill.objects.all()
# #     serializer_class = MedicineBillSerializer
# class MedicineBillViewSet(ModelViewSet):

#     queryset = MedicineBill.objects.all()
#     serializer_class = MedicineBillSerializer
#     permission_classes = [IsAuthenticated,IsPharmacist]

#     def create(self, request, *args, **kwargs):

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(
#             {
#                 "message": "Medicine bill created successfully",
#                 "data": serializer.data
#             },
#             status=status.HTTP_201_CREATED
#         )


# class SentPrescriptionListView(APIView):
#     permission_classes = [IsAuthenticated, IsPharmacist]

#     def get(self, request):
#         prescriptions = Prescription.objects.filter(
#             status="Sent"
#         ).select_related(
#             'consultation__appointment__patient',
#             'doctor'
#         ).prefetch_related('items__medicine_name')

#         serializer = IncomingPrescriptionSerializer(prescriptions, many=True)
#         return Response(
#             {
#                 "message": "Sent prescriptions fetched successfully",
#                 "count": prescriptions.count(),
#                 "data": serializer.data
#             },
#             status=status.HTTP_200_OK
#         )

# class SentPrescriptionDetailView(APIView):
#     permission_classes = [IsAuthenticated, IsPharmacist]

#     def get(self, request, prescription_code):
#         try:
#             prescription = Prescription.objects.select_related(
#                 'consultation__appointment__patient',
#                 'doctor'
#             ).prefetch_related('items__medicine_name').get(
#                 prescription_code=prescription_code,
#                 status="Sent"
#             )
#         except Prescription.DoesNotExist:
#             return Response(
#                 {"message": "Prescription not found or not yet sent"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = IncomingPrescriptionSerializer(prescription)
#         return Response(
#             {
#                 "message": "Prescription details fetched successfully",
#                 "data": serializer.data
#             },
#             status=status.HTTP_200_OK
#         )

# from rest_framework import viewsets, status
# from rest_framework.views import APIView
# from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.filters import SearchFilter
# from django_filters.rest_framework import DjangoFilterBackend
# from django.db import transaction

# from .models import (
#     Medicine, MedicineBatch, Dispense, DispenseItem, MedicineBill, MedicineStockLog
# )
# from .serializers import (
#     MedicineSerializer, MedicineBatchSerializer, DispenseSerializer, DispenseItemSerializer,
#     MedicineBillSerializer, MedicineStockLogSerializer, IncomingPrescriptionSerializer
# )
# from doctor.models import Prescription
# from authentication.permissions import IsPharmacist


# # ==============================
# # MEDICINE VIEWSET
# # ==============================
# class MedicineViewSet(ModelViewSet):
#     """
#     CRUD operations for medicines
#     """
#     queryset = Medicine.objects.all()
#     serializer_class = MedicineSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['name']
#     permission_classes = [IsAuthenticated, IsPharmacist]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {
#                 "message": "Medicine added successfully",
#                 "data": serializer.data
#             },
#             status=status.HTTP_201_CREATED
#         )

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {
#                 "message": "Medicine updated successfully",
#                 "data": serializer.data
#             }
#         )

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.delete()
#         return Response(
#             {"message": "Medicine deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT
#         )


# # ==============================
# # MEDICINE BATCH VIEWSET
# # ==============================
# class MedicineBatchViewSet(ModelViewSet):
#     """
#     CRUD operations for medicine batches
#     Supports filtering by medicine_id
#     """
#     queryset = MedicineBatch.objects.all().select_related('medicine')
#     serializer_class = MedicineBatchSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     filterset_fields = ['medicine']
#     search_fields = ['batch_number', 'medicine__name']
#     permission_classes = [IsAuthenticated, IsPharmacist]

#     def get_queryset(self):
#         """Add ordering by creation date"""
#         return super().get_queryset().order_by('-created_at')

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {
#                 "message": "Medicine batch added successfully",
#                 "data": serializer.data
#             },
#             status=status.HTTP_201_CREATED
#         )

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {
#                 "message": "Medicine batch updated successfully",
#                 "data": serializer.data
#             }
#         )

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.delete()
#         return Response(
#             {"message": "Medicine batch deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT
#         )


# # ==============================
# # DISPENSE VIEWSET
# # ==============================
# class DispenseViewSet(ModelViewSet):
#     """
#     CRUD operations for dispenses
#     Supports filtering by prescription and status
#     """
#     queryset = Dispense.objects.all().select_related(
#         'prescription__consultation__appointment__patient',
#         'prescription__doctor'
#     ).prefetch_related('items__batch__medicine')
#     serializer_class = DispenseSerializer
#     permission_classes = [IsAuthenticated, IsPharmacist]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['prescription', 'status', 'patient']

#     def get_queryset(self):
#         """Add ordering by dispense date"""
#         return super().get_queryset().order_by('-dispense_date')

#     @transaction.atomic
#     def create(self, request, *args, **kwargs):
#         """
#         Create a dispense with nested items
#         This is an atomic transaction
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         dispense = serializer.save()
        
#         return Response(
#             {
#                 "message": "Medicine dispensed successfully",
#                 "data": DispenseSerializer(dispense).data
#             },
#             status=status.HTTP_201_CREATED
#         )

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {
#                 "message": "Dispense updated successfully",
#                 "data": serializer.data
#             }
#         )

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.delete()
#         return Response(
#             {"message": "Dispense deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT
#         )


# # ==============================
# # DISPENSE ITEM VIEWSET (READ-ONLY)
# # ==============================
# class DispenseItemViewSet(ReadOnlyModelViewSet):
#     """
#     Read-only view for dispense items
#     """
#     queryset = DispenseItem.objects.all().select_related(
#         'dispense__prescription',
#         'batch__medicine'
#     )
#     serializer_class = DispenseItemSerializer
#     permission_classes = [IsAuthenticated, IsPharmacist]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['dispense']


# # ==============================
# # MEDICINE STOCK LOG VIEWSET (READ-ONLY)
# # ==============================
# class MedicineStockLogViewSet(ReadOnlyModelViewSet):
#     """
#     Read-only view for stock logs
#     """
#     queryset = MedicineStockLog.objects.all().select_related(
#         'batch__medicine'
#     )
#     serializer_class = MedicineStockLogSerializer
#     permission_classes = [IsAuthenticated, IsPharmacist]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['batch', 'change_type']

#     def get_queryset(self):
#         """Add ordering by creation date"""
#         return super().get_queryset().order_by('-created_at')


# # ==============================
# # MEDICINE BILL VIEWSET
# # ==============================
# class MedicineBillViewSet(ModelViewSet):
#     """
#     CRUD operations for medicine bills
#     """
#     queryset = MedicineBill.objects.all().select_related(
#         'dispense__prescription__consultation__appointment__patient'
#     )
#     serializer_class = MedicineBillSerializer
#     permission_classes = [IsAuthenticated, IsPharmacist]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['payment_status', 'dispense']

#     def get_queryset(self):
#         """Add ordering by creation date"""
#         return super().get_queryset().order_by('-created_at')

#     @transaction.atomic
#     def create(self, request, *args, **kwargs):
#         """
#         Create a medicine bill
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         bill = serializer.save()
        
#         return Response(
#             {
#                 "message": "Medicine bill created successfully",
#                 "data": MedicineBillSerializer(bill).data
#             },
#             status=status.HTTP_201_CREATED
#         )

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {
#                 "message": "Medicine bill updated successfully",
#                 "data": serializer.data
#             }
#         )

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.delete()
#         return Response(
#             {"message": "Medicine bill deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT
#         )


# # ==============================
# # SENT PRESCRIPTIONS LIST
# # ==============================
# class SentPrescriptionListView(APIView):
#     """
#     Get all prescriptions that have been sent to pharmacy
#     """
#     permission_classes = [IsAuthenticated, IsPharmacist]

#     def get(self, request):
#         prescriptions = Prescription.objects.filter(
#             status="Sent"
#         ).select_related(
#             'consultation__appointment__patient',
#             'doctor'
#         ).prefetch_related(
#             'items__medicine_name'
#         ).order_by('-sent_at')

#         serializer = IncomingPrescriptionSerializer(prescriptions, many=True)
        
#         return Response(
#             {
#                 "message": "Sent prescriptions fetched successfully",
#                 "count": prescriptions.count(),
#                 "data": serializer.data
#             },
#             status=status.HTTP_200_OK
#         )


# # ==============================
# # SENT PRESCRIPTION DETAIL
# # ==============================
# class SentPrescriptionDetailView(APIView):
#     """
#     Get details of a specific prescription by prescription_code
#     """
#     permission_classes = [IsAuthenticated, IsPharmacist]

#     def get(self, request, prescription_code):
#         try:
#             prescription = Prescription.objects.select_related(
#                 'consultation__appointment__patient',
#                 'doctor'
#             ).prefetch_related(
#                 'items__medicine_name'
#             ).get(
#                 prescription_code=prescription_code,
#                 status="Sent"
#             )
#         except Prescription.DoesNotExist:
#             return Response(
#                 {"message": "Prescription not found or not yet sent to pharmacy"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = IncomingPrescriptionSerializer(prescription)
        
#         return Response(
#             {
#                 "message": "Prescription details fetched successfully",
#                 "data": serializer.data
#             },
#             status=status.HTTP_200_OK
#         )

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from .models import (
    Medicine, MedicineBatch, Dispense, DispenseItem, MedicineBill, MedicineStockLog
)
from .serializers import (
    MedicineSerializer, MedicineBatchSerializer, DispenseSerializer, DispenseItemSerializer,
    MedicineBillSerializer, MedicineStockLogSerializer, IncomingPrescriptionSerializer
)
from doctor.models import Prescription
from authentication.permissions import IsPharmacist


# ==============================
# BASE PERMISSION (COMMON)
# ==============================
COMMON_PERMISSION = [IsAuthenticated, IsPharmacist]


# ==============================
# MEDICINE VIEWSET
# ==============================
class MedicineViewSet(ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    permission_classes = COMMON_PERMISSION

    def list(self, request, *args, **kwargs):
        """Return medicines in consistent format"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            "message": "Medicines fetched successfully",
            "count": queryset.count(),
            "data": serializer.data,
            "results": serializer.data  # Add for frontend compatibility
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Medicine added successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Medicine updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({
            "message": "Medicine deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


# ==============================
# MEDICINE BATCH VIEWSET
# ==============================
class MedicineBatchViewSet(ModelViewSet):
    queryset = MedicineBatch.objects.all().select_related('medicine')
    serializer_class = MedicineBatchSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['medicine']
    search_fields = ['batch_number', 'medicine__name']
    permission_classes = COMMON_PERMISSION

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        """Return batches in consistent format"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            "message": "Batches fetched successfully",
            "count": queryset.count(),
            "data": serializer.data,
            "results": serializer.data  # Add for frontend compatibility
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Medicine batch added successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


# ==============================
# DISPENSE VIEWSET
# ==============================
class DispenseViewSet(ModelViewSet):
    queryset = Dispense.objects.all().select_related(
        'prescription__consultation__appointment__patient',
        'prescription__doctor'
    ).prefetch_related('items__batch__medicine')

    serializer_class = DispenseSerializer
    permission_classes = COMMON_PERMISSION
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['prescription', 'status', 'patient']

    def get_queryset(self):
        return super().get_queryset().order_by('-dispense_date')

    def list(self, request, *args, **kwargs):
        """Return dispenses in consistent format"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            "message": "Dispenses fetched successfully",
            "count": queryset.count(),
            "data": serializer.data,
            "results": serializer.data
        }, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dispense = serializer.save()

        return Response({
            "message": "Medicine dispensed successfully",
            "data": DispenseSerializer(dispense).data
        }, status=status.HTTP_201_CREATED)


# ==============================
# DISPENSE ITEM VIEWSET
# ==============================
class DispenseItemViewSet(ReadOnlyModelViewSet):
    queryset = DispenseItem.objects.all().select_related(
        'dispense__prescription',
        'batch__medicine'
    )
    serializer_class = DispenseItemSerializer
    permission_classes = COMMON_PERMISSION
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['dispense']

    def list(self, request, *args, **kwargs):
        """Return dispense items in consistent format"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            "message": "Dispense items fetched successfully",
            "count": queryset.count(),
            "data": serializer.data,
            "results": serializer.data
        }, status=status.HTTP_200_OK)


# ==============================
# STOCK LOG VIEWSET
# ==============================
class MedicineStockLogViewSet(ReadOnlyModelViewSet):
    queryset = MedicineStockLog.objects.all().select_related('batch__medicine')
    serializer_class = MedicineStockLogSerializer
    permission_classes = COMMON_PERMISSION
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['batch', 'change_type']

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        """Return stock logs in consistent format"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            "message": "Stock logs fetched successfully",
            "count": queryset.count(),
            "data": serializer.data,
            "results": serializer.data
        }, status=status.HTTP_200_OK)


# ==============================
# MEDICINE BILL VIEWSET
# ==============================
class MedicineBillViewSet(ModelViewSet):
    queryset = MedicineBill.objects.all().select_related(
        'dispense__prescription__consultation__appointment__patient'
    )
    serializer_class = MedicineBillSerializer
    permission_classes = COMMON_PERMISSION
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payment_status', 'dispense']

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        """Return bills in consistent format"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            "message": "Bills fetched successfully",
            "count": queryset.count(),
            "data": serializer.data,
            "results": serializer.data  # Add for frontend compatibility
        }, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bill = serializer.save()

        return Response({
            "message": "Medicine bill created successfully",
            "data": MedicineBillSerializer(bill).data
        }, status=status.HTTP_201_CREATED)


# ==============================
# SENT PRESCRIPTIONS LIST
# ==============================
class SentPrescriptionListView(APIView):
    permission_classes = COMMON_PERMISSION

    def get(self, request):
        prescriptions = Prescription.objects.filter(
            status="Sent"
        ).select_related(
            'consultation__appointment__patient',
            'doctor'
        ).prefetch_related(
            'items__medicine_name'
        ).order_by('-sent_at')

        serializer = IncomingPrescriptionSerializer(prescriptions, many=True)

        return Response({
            "message": "Sent prescriptions fetched successfully",
            "count": prescriptions.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# ==============================
# SENT PRESCRIPTION DETAIL
# ==============================
class SentPrescriptionDetailView(APIView):
    permission_classes = COMMON_PERMISSION

    def get(self, request, prescription_code):
        try:
            prescription = Prescription.objects.select_related(
                'consultation__appointment__patient',
                'doctor'
            ).prefetch_related(
                'items__medicine_name'
            ).get(
                prescription_code=prescription_code,
                status="Sent"
            )

        except Prescription.DoesNotExist:
            return Response(
                {"message": "Prescription not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = IncomingPrescriptionSerializer(prescription)

        return Response({
            "message": "Prescription details fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)