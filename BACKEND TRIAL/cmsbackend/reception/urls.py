from rest_framework import routers
from django.urls import path, include
from .views import PatientViewSet, DoctorAvailabilityViewSet, AppointmentViewSet, ConsultationBillViewSet

router = routers.DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'doctor-availability', DoctorAvailabilityViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'consultation-bills', ConsultationBillViewSet)

urlpatterns = [
    path('', include(router.urls)),
]