from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StaffProfileViewSet,
    DoctorProfileViewSet,
    ReceptionistProfileViewSet,
    LabTechnicianProfileViewSet,
    PharmacistProfileViewSet,
    AuditLogViewSet
)

router = DefaultRouter()
router.register(r'staff', StaffProfileViewSet, basename='staff')
router.register(r'doctors', DoctorProfileViewSet, basename='doctor')
router.register(r'receptionists', ReceptionistProfileViewSet, basename='receptionist')
router.register(r'labtechnicians', LabTechnicianProfileViewSet, basename='labtechnician')
router.register(r'pharmacists', PharmacistProfileViewSet, basename='pharmacist')
router.register(r'auditlogs', AuditLogViewSet, basename='auditlog')

urlpatterns = [
    path('api/', include(router.urls)),
]