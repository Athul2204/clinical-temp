# cmsbackend/pharmacist/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicineViewSet, MedicineBatchViewSet, DispenseViewSet, DispenseItemViewSet, MedicineBillViewSet

router = DefaultRouter()
router.register(r'medicines', MedicineViewSet, basename='medicine')
router.register(r'batches', MedicineBatchViewSet, basename='batch')
router.register(r'dispenses', DispenseViewSet, basename='dispense')
router.register(r'dispense-items', DispenseItemViewSet, basename='dispenseitem')
router.register(r'bills', MedicineBillViewSet, basename='medicinebill')

urlpatterns = [
    path('', include(router.urls)),
]