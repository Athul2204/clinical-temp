from django.urls import path
from .views import (
    StaffListView,
    CreateStaffView,
    DoctorListView,
    CreateDoctorView,
    ReceptionistListView,
    CreateReceptionistView,
    LabTechnicianListView,
    CreateLabTechnicianView,
    PharmacistListView,
    CreatePharmacistView,
    AuditLogListView
)

urlpatterns = [

    # Staff
    path('staff/', StaffListView.as_view()),
    path('staff/create/', CreateStaffView.as_view()),

    # Doctor
    path('doctors/', DoctorListView.as_view()),
    path('doctors/create/', CreateDoctorView.as_view()),

    # Receptionist
    path('receptionists/', ReceptionistListView.as_view()),
    path('receptionists/create/', CreateReceptionistView.as_view()),

    # Lab Technician
    path('lab-technicians/', LabTechnicianListView.as_view()),
    path('lab-technicians/create/', CreateLabTechnicianView.as_view()),

    # Pharmacist
    path('pharmacists/', PharmacistListView.as_view()),
    path('pharmacists/create/', CreatePharmacistView.as_view()),

    # Audit Logs
    path('audit-logs/', AuditLogListView.as_view()),

]