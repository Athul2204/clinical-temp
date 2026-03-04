from rest_framework import routers
from django.urls import path, include
from .views import ConsultationViewSet, PrescriptionViewSet, PrescriptionItemViewSet, LabTestRequestViewSet, LabTestRequestItemViewSet

router = routers.DefaultRouter()
router.register(r'consultations', ConsultationViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'prescription-items', PrescriptionItemViewSet)
router.register(r'lab-requests', LabTestRequestViewSet)
router.register(r'lab-request-items', LabTestRequestItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]