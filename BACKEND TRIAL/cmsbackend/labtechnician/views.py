

# from rest_framework import viewsets, status
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# from .models import (
#     LabTest,
#     LabOrder,
#     LabOrderItem,
#     LabResult,
#     LabBill,
#     LabEquipment,
#     LabMaintenance
# )

# from .serializers import (
#     LabTestSerializer,
#     LabOrderSerializer,
#     LabOrderItemSerializer,
#     LabResultSerializer,
#     LabBillSerializer,
#     LabEquipmentSerializer,
#     LabMaintenanceSerializer
# )


# # ==============================
# # LAB TEST
# # ==============================

# class LabTechnicianBaseViewSet(viewsets.ModelViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

# class LabTestViewSet(LabTechnicianBaseViewSet):

#     queryset = LabTest.objects.all()
#     serializer_class = LabTestSerializer

#     def list(self, request):
#         tests = self.get_queryset()
#         serializer = self.get_serializer(tests, many=True)

#         return Response({
#             "message": "Lab tests fetched successfully",
#             "count": tests.count(),
#             "data": serializer.data
#         })

#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             test = serializer.save()
#             return Response({
#                 "message": "Lab test created successfully",
#                 "test_id": test.test_id
#             }, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ==============================
# # LAB ORDER
# # ==============================

# class LabOrderViewSet(LabTechnicianBaseViewSet):

#     queryset = LabOrder.objects.all()
#     serializer_class = LabOrderSerializer

#     def list(self, request):
#         orders = self.get_queryset()
#         serializer = self.get_serializer(orders, many=True)

#         return Response({
#             "message": "Lab orders fetched successfully",
#             "count": orders.count(),
#             "data": serializer.data
#         })


# # ==============================
# # LAB ORDER ITEM
# # ==============================

# class LabOrderItemViewSet(LabTechnicianBaseViewSet):

#     queryset = LabOrderItem.objects.all()
#     serializer_class = LabOrderItemSerializer

#     def list(self, request):
#         items = self.get_queryset()
#         serializer = self.get_serializer(items, many=True)

#         return Response({
#             "message": "Lab order items fetched successfully",
#             "count": items.count(),
#             "data": serializer.data
#         })


# # ==============================
# # LAB RESULT
# # ==============================

# class LabResultViewSet(LabTechnicianBaseViewSet):

#     queryset = LabResult.objects.all()
#     serializer_class = LabResultSerializer

#     def list(self, request):
#         results = self.get_queryset()
#         serializer = self.get_serializer(results, many=True)

#         return Response({
#             "message": "Lab results fetched successfully",
#             "count": results.count(),
#             "data": serializer.data
#         })


# # ==============================
# # LAB BILL
# # ==============================

# class LabBillViewSet(LabTechnicianBaseViewSet):

#     queryset = LabBill.objects.all()
#     serializer_class = LabBillSerializer

#     def list(self, request):
#         bills = self.get_queryset()
#         serializer = self.get_serializer(bills, many=True)

#         return Response({
#             "message": "Lab bills fetched successfully",
#             "count": bills.count(),
#             "data": serializer.data
#         })


# # ==============================
# # LAB EQUIPMENT
# # ==============================

# class LabEquipmentViewSet(LabTechnicianBaseViewSet):

#     queryset = LabEquipment.objects.all()
#     serializer_class = LabEquipmentSerializer

#     def list(self, request):
#         equipment = self.get_queryset()
#         serializer = self.get_serializer(equipment, many=True)

#         return Response({
#             "message": "Lab equipment fetched successfully",
#             "count": equipment.count(),
#             "data": serializer.data
#         })


# # ==============================
# # LAB MAINTENANCE
# # ==============================

# class LabMaintenanceViewSet(LabTechnicianBaseViewSet):

#     queryset = LabMaintenance.objects.all()
#     serializer_class = LabMaintenanceSerializer

#     def list(self, request):
#         records = self.get_queryset()
#         serializer = self.get_serializer(records, many=True)

#         return Response({
#             "message": "Maintenance records fetched successfully",
#             "count": records.count(),
#             "data": serializer.data
#         })


from rest_framework import viewsets, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction

from .models import (
    LabTest, LabOrder, LabOrderItem, LabResult, LabBill, LabEquipment, LabMaintenance
)
from .serializers import (
    LabTestSerializer, LabOrderSerializer, LabOrderItemSerializer, LabResultSerializer,
    LabBillSerializer, LabEquipmentSerializer, LabMaintenanceSerializer
)


# ==============================
# BASE VIEWSET
# ==============================
class LabTechnicianBaseViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


# ==============================
# LAB TEST
# ==============================
class LabTestViewSet(LabTechnicianBaseViewSet):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer

    def list(self, request):
        tests = self.get_queryset()
        serializer = self.get_serializer(tests, many=True)
        return Response({"message": "Lab tests fetched successfully", "count": tests.count(), "data": serializer.data})

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        test = serializer.save()
        return Response({"message": "Lab test created successfully", "test_id": test.test_id}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Lab test updated successfully", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Lab test deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ==============================
# LAB ORDER
# ==============================
class LabOrderViewSet(LabTechnicianBaseViewSet):
    queryset = LabOrder.objects.all()
    serializer_class = LabOrderSerializer

    def list(self, request):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response({"message": "Lab orders fetched successfully", "count": orders.count(), "data": serializer.data})

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response({"message": "Lab order created successfully", "order_id": order.order_id}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Lab order updated successfully", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Lab order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ==============================
# LAB ORDER ITEM
# ==============================
class LabOrderItemViewSet(LabTechnicianBaseViewSet):
    queryset = LabOrderItem.objects.all()
    serializer_class = LabOrderItemSerializer

    def list(self, request):
        items = self.get_queryset()
        serializer = self.get_serializer(items, many=True)
        return Response({"message": "Lab order items fetched successfully", "count": items.count(), "data": serializer.data})


# ==============================
# LAB RESULT
# ==============================
class LabResultViewSet(LabTechnicianBaseViewSet):
    queryset = LabResult.objects.all()
    serializer_class = LabResultSerializer

    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response({"message": "Lab result created successfully", "result_id": result.result_id}, status=status.HTTP_201_CREATED)

    def list(self, request):
        results = self.get_queryset()
        serializer = self.get_serializer(results, many=True)
        return Response({"message": "Lab results fetched successfully", "count": results.count(), "data": serializer.data})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Lab result updated successfully", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Lab result deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ==============================
# LAB BILL
# ==============================
class LabBillViewSet(LabTechnicianBaseViewSet):
    queryset = LabBill.objects.all()
    serializer_class = LabBillSerializer

    def list(self, request):
        bills = self.get_queryset()
        serializer = self.get_serializer(bills, many=True)
        return Response({"message": "Lab bills fetched successfully", "count": bills.count(), "data": serializer.data})

    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bill = serializer.save()
        return Response({"message": "Lab bill created successfully", "bill_id": bill.lab_bill_id}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Lab bill updated successfully", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Lab bill deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ==============================
# LAB EQUIPMENT
# ==============================
class LabEquipmentViewSet(LabTechnicianBaseViewSet):
    queryset = LabEquipment.objects.all()
    serializer_class = LabEquipmentSerializer

    def list(self, request):
        equipment = self.get_queryset()
        serializer = self.get_serializer(equipment, many=True)
        return Response({"message": "Lab equipment fetched successfully", "count": equipment.count(), "data": serializer.data})

    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        eq = serializer.save()
        return Response({"message": "Lab equipment added successfully", "equipment_id": eq.equipment_id}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Lab equipment updated successfully", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Lab equipment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ==============================
# LAB MAINTENANCE
# ==============================
class LabMaintenanceViewSet(LabTechnicianBaseViewSet):
    queryset = LabMaintenance.objects.all()
    serializer_class = LabMaintenanceSerializer

    def list(self, request):
        records = self.get_queryset()
        serializer = self.get_serializer(records, many=True)
        return Response({"message": "Maintenance records fetched successfully", "count": records.count(), "data": serializer.data})

    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        record = serializer.save()
        return Response({"message": "Maintenance record added successfully", "maintenance_id": record.maintenance_id}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Maintenance record updated successfully", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Maintenance record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)