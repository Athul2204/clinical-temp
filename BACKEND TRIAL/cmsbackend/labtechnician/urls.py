from rest_framework import routers
from django.urls import path, include
from .views import LabTestViewSet, LabOrderViewSet, LabOrderItemViewSet, LabResultViewSet, LabBillViewSet, LabEquipmentViewSet, LabMaintenanceViewSet

# router = routers.DefaultRouter()
# router.register(r'lab-tests', LabTestViewSet)
# router.register(r'lab-orders', LabOrderViewSet)
# router.register(r'lab-order-items', LabOrderItemViewSet)
# router.register(r'lab-results', LabResultViewSet)
# router.register(r'lab-bills', LabBillViewSet)
# router.register(r'lab-equipment', LabEquipmentViewSet)
# router.register(r'lab-maintenance', LabMaintenanceViewSet)

urlpatterns = [

    path(
        "lab-tests/",
        LabTestViewSet.as_view({"get": "list", "post": "create"}),
        name="lab-tests"
    ),

    path(
        "lab-orders/",
        LabOrderViewSet.as_view({"get": "list", "post": "create"}),
        name="lab-orders"
    ),

    path(
        "lab-order-items/",
        LabOrderItemViewSet.as_view({"get": "list", "post": "create"}),
        name="lab-order-items"
    ),

    path(
        "lab-results/",
        LabResultViewSet.as_view({"get": "list", "post": "create"}),
        name="lab-results"
    ),

    path(
        "lab-bills/",
        LabBillViewSet.as_view({"get": "list", "post": "create"}),
        name="lab-bills"
    ),

    path(
        "lab-equipment/",
        LabEquipmentViewSet.as_view({"get": "list", "post": "create"}),
        name="lab-equipment"
    ),

    path(
        "lab-maintenance/",
        LabMaintenanceViewSet.as_view({"get": "list", "post": "create"}),
        name="lab-maintenance"
    ),

]