from rest_framework import routers
from django.urls import path, include
from .views import LabTestViewSet, LabOrderViewSet, LabOrderItemViewSet, LabResultViewSet, LabBillViewSet, LabEquipmentViewSet, LabMaintenanceViewSet

router = routers.DefaultRouter()
router.register(r'lab-tests', LabTestViewSet)
router.register(r'lab-orders', LabOrderViewSet)
router.register(r'lab-order-items', LabOrderItemViewSet)
router.register(r'lab-results', LabResultViewSet)
router.register(r'lab-bills', LabBillViewSet)
router.register(r'lab-equipment', LabEquipmentViewSet)
router.register(r'lab-maintenance', LabMaintenanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]