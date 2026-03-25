# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from .models import LabTest, LabOrder, LabOrderItem, LabResult, LabBill, LabEquipment, LabMaintenance
# from .serializers import LabTestSerializer, LabOrderSerializer, LabOrderItemSerializer, LabResultSerializer, LabBillSerializer, LabEquipmentSerializer, LabMaintenanceSerializer

# class LabTestViewSet(viewsets.ModelViewSet):
#     queryset = LabTest.objects.all()
#     serializer_class = LabTestSerializer
#     permission_classes = [IsAuthenticated]

# class LabOrderViewSet(viewsets.ModelViewSet):
#     queryset = LabOrder.objects.all()
#     serializer_class = LabOrderSerializer
#     permission_classes = [IsAuthenticated]

# class LabOrderItemViewSet(viewsets.ModelViewSet):
#     queryset = LabOrderItem.objects.all()
#     serializer_class = LabOrderItemSerializer
#     permission_classes = [IsAuthenticated]

# class LabResultViewSet(viewsets.ModelViewSet):
#     queryset = LabResult.objects.all()
#     serializer_class = LabResultSerializer
#     permission_classes = [IsAuthenticated]

# class LabBillViewSet(viewsets.ModelViewSet):
#     queryset = LabBill.objects.all()
#     serializer_class = LabBillSerializer
#     permission_classes = [IsAuthenticated]

# class LabEquipmentViewSet(viewsets.ModelViewSet):
#     queryset = LabEquipment.objects.all()
#     serializer_class = LabEquipmentSerializer
#     permission_classes = [IsAuthenticated]

# class LabMaintenanceViewSet(viewsets.ModelViewSet):
#     queryset = LabMaintenance.objects.all()
#     serializer_class = LabMaintenanceSerializer
#     permission_classes = [IsAuthenticated]


from rest_framework import viewsets, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    LabTest,
    LabOrder,
    LabOrderItem,
    LabResult,
    LabBill,
    LabEquipment,
    LabMaintenance
)

from .serializers import (
    LabTestSerializer,
    LabOrderSerializer,
    LabOrderItemSerializer,
    LabResultSerializer,
    LabBillSerializer,
    LabEquipmentSerializer,
    LabMaintenanceSerializer
)


# ==============================
# LAB TEST
# ==============================

class LabTechnicianBaseViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class LabTestViewSet(LabTechnicianBaseViewSet):

    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer

    def list(self, request):
        tests = self.get_queryset()
        serializer = self.get_serializer(tests, many=True)

        return Response({
            "message": "Lab tests fetched successfully",
            "count": tests.count(),
            "data": serializer.data
        })

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            test = serializer.save()
            return Response({
                "message": "Lab test created successfully",
                "test_id": test.test_id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==============================
# LAB ORDER
# ==============================

class LabOrderViewSet(LabTechnicianBaseViewSet):

    queryset = LabOrder.objects.all()
    serializer_class = LabOrderSerializer

    def list(self, request):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)

        return Response({
            "message": "Lab orders fetched successfully",
            "count": orders.count(),
            "data": serializer.data
        })


# ==============================
# LAB ORDER ITEM
# ==============================

class LabOrderItemViewSet(LabTechnicianBaseViewSet):

    queryset = LabOrderItem.objects.all()
    serializer_class = LabOrderItemSerializer

    def list(self, request):
        items = self.get_queryset()
        serializer = self.get_serializer(items, many=True)

        return Response({
            "message": "Lab order items fetched successfully",
            "count": items.count(),
            "data": serializer.data
        })


# ==============================
# LAB RESULT
# ==============================

class LabResultViewSet(LabTechnicianBaseViewSet):

    queryset = LabResult.objects.all()
    serializer_class = LabResultSerializer

    def list(self, request):
        results = self.get_queryset()
        serializer = self.get_serializer(results, many=True)

        return Response({
            "message": "Lab results fetched successfully",
            "count": results.count(),
            "data": serializer.data
        })


# ==============================
# LAB BILL
# ==============================

class LabBillViewSet(LabTechnicianBaseViewSet):

    queryset = LabBill.objects.all()
    serializer_class = LabBillSerializer

    def list(self, request):
        bills = self.get_queryset()
        serializer = self.get_serializer(bills, many=True)

        return Response({
            "message": "Lab bills fetched successfully",
            "count": bills.count(),
            "data": serializer.data
        })


# ==============================
# LAB EQUIPMENT
# ==============================

class LabEquipmentViewSet(LabTechnicianBaseViewSet):

    queryset = LabEquipment.objects.all()
    serializer_class = LabEquipmentSerializer

    def list(self, request):
        equipment = self.get_queryset()
        serializer = self.get_serializer(equipment, many=True)

        return Response({
            "message": "Lab equipment fetched successfully",
            "count": equipment.count(),
            "data": serializer.data
        })


# ==============================
# LAB MAINTENANCE
# ==============================

class LabMaintenanceViewSet(LabTechnicianBaseViewSet):

    queryset = LabMaintenance.objects.all()
    serializer_class = LabMaintenanceSerializer

    def list(self, request):
        records = self.get_queryset()
        serializer = self.get_serializer(records, many=True)

        return Response({
            "message": "Maintenance records fetched successfully",
            "count": records.count(),
            "data": serializer.data
        })