from django.urls import path
from .views import (
    TodayAppointmentsView,
    ConsultationPageView,
    CreateConsultationView,
    CreateLabTestRequestView,
    ViewLabResults,
    MarkLabResultsViewedView,
    CompleteConsultationView,
    CreatePrescriptionView,
    LabTestListView,
    MedicineListView
)


urlpatterns = [
    path(
        "today-appointments/",
        TodayAppointmentsView.as_view(),
        name="today-appointments"
    ),
    path(
        "consultation/<int:appointment_id>/",
        ConsultationPageView.as_view(),
        name="consultation-page"
    ),
    path(
        "consultations/",
        CreateConsultationView.as_view(),
        name="create-consultation"
    ),
    path(
        "lab-test-request/",
        CreateLabTestRequestView.as_view(),
        name="lab-test-request"
    ),
    path(
        "lab-results/<int:consultation_id>/",
        ViewLabResults.as_view(),
        name="view-lab-results"
    ),
    # ✅ NEW: Doctor marks lab results as explicitly viewed
    path(
        "lab-results/<int:lab_request_id>/mark-viewed/",
        MarkLabResultsViewedView.as_view(),
        name="mark-lab-results-viewed"
    ),
    # ✅ Doctor marks consultation as Completed (after prescription written)
    path(
        "consultation/<int:appointment_id>/complete/",
        CompleteConsultationView.as_view(),
        name="complete-consultation"
    ),
    path(
        "prescriptions/",
        CreatePrescriptionView.as_view(),
        name="create-prescription"
    ),
    path(
    "lab-tests/",
    LabTestListView.as_view(),
    name="lab-tests"
),
path("medicines/", MedicineListView.as_view(), name="medicine-list"),
]