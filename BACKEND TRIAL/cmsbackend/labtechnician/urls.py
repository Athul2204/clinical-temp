from django.urls import path
from .views import (
    LabTestViewSet,
    LabOrderViewSet,
    LabOrderItemViewSet,
    LabResultViewSet,
    LabBillViewSet,
    LabEquipmentViewSet,
    LabMaintenanceViewSet,
    IncomingLabRequestsView,
)

urlpatterns = [

    # ── LAB TESTS ──────────────────────────────────────────────────
    path(
        "lab-tests/",
        LabTestViewSet.as_view({"get": "list", "post": "create"}),
        name="lab-tests"
    ),
    path(
        "lab-tests/<int:pk>/",
        LabTestViewSet.as_view({"put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="lab-test-detail"
    ),

    # ── INCOMING LAB REQUESTS (from Doctor) ────────────────────────
    path(
        "lab-requests/",
        IncomingLabRequestsView.as_view({"get": "list"}),
        name="lab-requests"
    ),

    # ── LAB ORDERS ─────────────────────────────────────────────────
    path(
        "lab-orders/",
        LabOrderViewSet.as_view({"get": "list", "post": "create"}),
        name="lab-orders"
    ),
    path(
        "lab-orders/<int:pk>/",
        LabOrderViewSet.as_view({"put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="lab-order-detail"
    ),

    # ── LAB ORDER ITEMS ────────────────────────────────────────────
    path(
        "lab-order-items/",
        LabOrderItemViewSet.as_view({"get": "list", "post": "create"}),
        name="lab-order-items"
    ),
    path(
        "lab-order-items/<int:pk>/",
        LabOrderItemViewSet.as_view({"put": "update", "delete": "destroy"}),
        name="lab-order-item-detail"
    ),

    # ── LAB RESULTS ────────────────────────────────────────────────
    path(
        "lab-results/",
        LabResultViewSet.as_view({"get": "list", "post": "create"}),
        name="lab-results"
    ),
    path(
        "lab-results/<int:pk>/",
        LabResultViewSet.as_view({"put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="lab-result-detail"
    ),

    # ── LAB BILLS ──────────────────────────────────────────────────
    path(
        "lab-bills/",
        LabBillViewSet.as_view({"get": "list", "post": "create"}),
        name="lab-bills"
    ),
    path(
        "lab-bills/<int:pk>/",
        LabBillViewSet.as_view({"put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="lab-bill-detail"
    ),

    # ── LAB EQUIPMENT ──────────────────────────────────────────────
    path(
        "lab-equipment/",
        LabEquipmentViewSet.as_view({"get": "list", "post": "create"}),
        name="lab-equipment"
    ),
    path(
        "lab-equipment/<int:pk>/",
        LabEquipmentViewSet.as_view({"put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="lab-equipment-detail"
    ),

    # ── LAB MAINTENANCE ────────────────────────────────────────────
    path(
        "lab-maintenance/",
        LabMaintenanceViewSet.as_view({"get": "list", "post": "create"}),
        name="lab-maintenance"
    ),
    path(
        "lab-maintenance/<int:pk>/",
        LabMaintenanceViewSet.as_view({"put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="lab-maintenance-detail"
    ),

]