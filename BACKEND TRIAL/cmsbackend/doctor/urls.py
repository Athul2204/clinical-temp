from django.urls import path
from .views import TodayAppointmentsView,ConsultationPageView,CreateConsultationView, CreateLabTestRequestView
from .views import ViewLabResults,CreatePrescriptionView


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
    path(
        "prescriptions/",
        CreatePrescriptionView.as_view(),
        name="create-prescription"
    ),
]

#