from rest_framework import viewsets, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from rest_framework.decorators import action

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
        return Response({
            "message": "Lab tests fetched successfully",
            "count": tests.count(),
            "data": serializer.data
        })

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        test = serializer.save()
        return Response({
            "message": "Lab test created successfully",
            "test_id": test.test_id,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Lab test updated successfully",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "message": "Lab test deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


# ==============================
# INCOMING LAB REQUESTS (from Doctor)
# ==============================
class IncomingLabRequestsView(LabTechnicianBaseViewSet):
    """
    Returns all LabTestRequests from doctors so the lab technician
    can see pending tests and create lab orders with one click.
    """
    http_method_names = ["get"]

    def list(self, request):
        from doctor.models import LabTestRequest

        requests_qs = LabTestRequest.objects.select_related(
            "consultation__appointment__patient",
            "doctor__staff"
        ).prefetch_related("tests__lab_test").order_by("-created_at")

        data = []
        for lr in requests_qs:
            patient = lr.consultation.appointment.patient
            already_created = lr.lab_orders.exists()

            tests = [
                {
                    "item_id": item.id,
                    "test_id": item.lab_test.test_id,
                    "test_name": item.lab_test.test_name,
                    "test_cost": str(item.lab_test.cost) if item.lab_test.cost else None,
                    "test_normal_range": item.lab_test.normal_range,
                    "test_unit": item.lab_test.unit,
                }
                for item in lr.tests.all()
            ]

            doctor_name = ""
            try:
                s = lr.doctor.staff
                doctor_name = f"{s.first_name} {s.last_name}".strip()
            except Exception:
                doctor_name = f"Doctor #{lr.doctor_id}"

            data.append({
                "lab_request_id": lr.id,
                "status": lr.status,
                "notes": lr.notes,
                "created_at": lr.created_at,
                "already_created": already_created,
                "doctor_name": doctor_name,
                "patient_id": patient.patient_id,
                "patient_name": f"{patient.first_name} {patient.last_name}".strip(),
                "tests": tests,
            })

        return Response({
            "message": "Lab requests fetched successfully",
            "count": len(data),
            "data": data
        })


# ==============================
# LAB ORDER
# ==============================
class LabOrderViewSet(LabTechnicianBaseViewSet):
    queryset = LabOrder.objects.select_related('patient', 'lab_request').prefetch_related('items__lab_test').all()
    serializer_class = LabOrderSerializer

    def list(self, request):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response({
            "message": "Lab orders fetched successfully",
            "count": orders.count(),
            "data": serializer.data
        })

    @transaction.atomic
    def create(self, request):
        """
        Create a lab order from a lab request.
        Auto-creates LabOrderItems from the linked LabTestRequest tests.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Auto-create LabOrderItems from the linked LabTestRequest tests
        for request_item in order.lab_request.tests.all():
            LabOrderItem.objects.get_or_create(
                lab_order=order,
                lab_test=request_item.lab_test
            )

        # Refresh to get the items
        order.refresh_from_db()
        response_serializer = self.get_serializer(order)

        return Response({
            "message": "Lab order created successfully",
            "order_id": order.order_id,
            "data": response_serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Lab order updated successfully",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "message": "Lab order deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


# ==============================
# LAB ORDER ITEM
# ==============================
class LabOrderItemViewSet(LabTechnicianBaseViewSet):
    queryset = LabOrderItem.objects.select_related('lab_order', 'lab_test').all()
    serializer_class = LabOrderItemSerializer

    def list(self, request):
        items = self.get_queryset()
        serializer = self.get_serializer(items, many=True)
        return Response({
            "message": "Lab order items fetched successfully",
            "count": items.count(),
            "data": serializer.data
        })

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return Response({
            "message": "Lab order item created successfully",
            "order_item_id": item.order_item_id,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


# ==============================
# LAB RESULT
# ==============================
class LabResultViewSet(LabTechnicianBaseViewSet):
    queryset = LabResult.objects.select_related(
        'lab_order_item__lab_order__patient',
        'lab_order_item__lab_test'
    ).all()
    serializer_class = LabResultSerializer

    def list(self, request):
        results = self.get_queryset()
        serializer = self.get_serializer(results, many=True)
        return Response({
            "message": "Lab results fetched successfully",
            "count": results.count(),
            "data": serializer.data
        })

    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response({
            "message": "Lab result created successfully",
            "result_id": result.result_id,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Lab result updated successfully",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "message": "Lab result deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


# ==============================
# LAB BILL
# ==============================
class LabBillViewSet(LabTechnicianBaseViewSet):
    queryset = LabBill.objects.select_related('lab_order__patient').all()
    serializer_class = LabBillSerializer

    def list(self, request):
        bills = self.get_queryset()
        serializer = self.get_serializer(bills, many=True)
        return Response({
            "message": "Lab bills fetched successfully",
            "count": bills.count(),
            "data": serializer.data
        })

    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bill = serializer.save()
        return Response({
            "message": "Lab bill created successfully",
            "bill_id": bill.lab_bill_id,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Lab bill updated successfully",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "message": "Lab bill deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


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

    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        eq = serializer.save()
        return Response({
            "message": "Lab equipment added successfully",
            "equipment_id": eq.equipment_id,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Lab equipment updated successfully",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "message": "Lab equipment deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


# ==============================
# LAB MAINTENANCE
# ==============================
class LabMaintenanceViewSet(LabTechnicianBaseViewSet):
    queryset = LabMaintenance.objects.select_related('equipment').all()
    serializer_class = LabMaintenanceSerializer

    def list(self, request):
        records = self.get_queryset()
        serializer = self.get_serializer(records, many=True)
        return Response({
            "message": "Maintenance records fetched successfully",
            "count": records.count(),
            "data": serializer.data
        })

    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        record = serializer.save()
        return Response({
            "message": "Maintenance record added successfully",
            "maintenance_id": record.maintenance_id,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Maintenance record updated successfully",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "message": "Maintenance record deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)