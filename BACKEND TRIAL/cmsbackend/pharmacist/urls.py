# cmsbackend/pharmacist/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicineViewSet, DispenseItemViewSet,MedicineStockLogViewSet,MedicineBatchViewSet, DispenseViewSet, MedicineBillViewSet
from .views import SentPrescriptionListView, SentPrescriptionDetailView

router = DefaultRouter()
router.register(r'medicines', MedicineViewSet, basename='medicine')
router.register(r'batches', MedicineBatchViewSet, basename='batch')
router.register(r'dispenses', DispenseViewSet, basename='dispense')
#router.register(r'dispense-items', DispenseItemViewSet, basename='dispenseitem')
router.register(r'bills', MedicineBillViewSet, basename='medicinebill')
router.register(r'dispense-items', DispenseItemViewSet, basename='dispense-items')
router.register(r'stock-logs', MedicineStockLogViewSet, basename='stock-logs')

urlpatterns = [
    path('', include(router.urls)),
    path('incoming-prescriptions/', SentPrescriptionListView.as_view(), name='incoming-prescriptions'),
    path('incoming-prescriptions/<str:prescription_code>/', SentPrescriptionDetailView.as_view(), name='incoming-prescription-detail'),
]