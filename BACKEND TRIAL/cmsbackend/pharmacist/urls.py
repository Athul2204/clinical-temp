# cmsbackend/pharmacist/urls.py

from django.urls import path
from .views import (
    MedicineViewSet,
    MedicineBatchViewSet,
    DispenseViewSet,
    DispenseItemViewSet,
    MedicineBillViewSet,
    MedicineStockLogViewSet,
    SentPrescriptionListView,
    SentPrescriptionDetailView,
)

urlpatterns = [

    # ── MEDICINES ────────────────────────────────────────────────
    path(
        "medicines/",
        MedicineViewSet.as_view({"get": "list", "post": "create"}),
        name="medicines"
    ),
    path(
        "medicines/<int:pk>/",
        MedicineViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy"
        }),
        name="medicine-detail"
    ),

    # ── MEDICINE BATCHES ─────────────────────────────────────────
    path(
        "batches/",
        MedicineBatchViewSet.as_view({"get": "list", "post": "create"}),
        name="batches"
    ),
    path(
        "batches/<int:pk>/",
        MedicineBatchViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy"
        }),
        name="batch-detail"
    ),

    # ── DISPENSE ─────────────────────────────────────────────────
    path(
        "dispenses/",
        DispenseViewSet.as_view({"get": "list", "post": "create"}),
        name="dispenses"
    ),
    path(
        "dispenses/<int:pk>/",
        DispenseViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy"
        }),
        name="dispense-detail"
    ),

    # ── DISPENSE ITEMS (READ-ONLY) ───────────────────────────────
    path(
        "dispense-items/",
        DispenseItemViewSet.as_view({"get": "list"}),
        name="dispense-items"
    ),
    path(
        "dispense-items/<int:pk>/",
        DispenseItemViewSet.as_view({"get": "retrieve"}),
        name="dispense-item-detail"
    ),

    # ── MEDICINE BILLS ───────────────────────────────────────────
    path(
        "bills/",
        MedicineBillViewSet.as_view({"get": "list", "post": "create"}),
        name="bills"
    ),
    path(
        "bills/<int:pk>/",
        MedicineBillViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy"
        }),
        name="bill-detail"
    ),

    # ── STOCK LOGS (READ-ONLY) ───────────────────────────────────
    path(
        "stock-logs/",
        MedicineStockLogViewSet.as_view({"get": "list"}),
        name="stock-logs"
    ),
    path(
        "stock-logs/<int:pk>/",
        MedicineStockLogViewSet.as_view({"get": "retrieve"}),
        name="stock-log-detail"
    ),

    # ── INCOMING PRESCRIPTIONS ───────────────────────────────────
    path(
        "incoming-prescriptions/",
        SentPrescriptionListView.as_view(),
        name="incoming-prescriptions"
    ),
    path(
        "incoming-prescriptions/<str:prescription_code>/",
        SentPrescriptionDetailView.as_view(),
        name="incoming-prescription-detail"
    ),
]