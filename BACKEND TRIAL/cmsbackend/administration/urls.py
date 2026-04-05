# administration/urls.py
from django.urls import path
from .views import (
    AdminDashboardView,
    StaffListView, StaffDetailView,
    DoctorListView, DoctorDetailView,
    ReceptionistListView, ReceptionistDetailView,
    LabTechnicianListView, LabTechnicianDetailView,
    PharmacistListView, PharmacistDetailView,
    AuditLogListView,
    DoctorSelfView,
    ReceptionistSelfView,
    PharmacistSelfView,
    LabTechnicianSelfView,
)

urlpatterns = [
    # Dashboard — admin only
    path("dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),

    # Staff — admin only
    path("staff/",          StaffListView.as_view(),   name="staff-list"),
    path("staff/<int:pk>/", StaffDetailView.as_view(), name="staff-detail"),

    # Doctors — GET: any authenticated | write: admin only
    path("doctor/",          DoctorListView.as_view(),   name="doctor-list"),
    path("doctor/<int:pk>/", DoctorDetailView.as_view(), name="doctor-detail"),
    path("doctor/me/",       DoctorSelfView.as_view(),   name="doctor-self"),

    # Receptionists — admin only
    path("receptionist/",          ReceptionistListView.as_view(),   name="receptionist-list"),
    path("receptionist/<int:pk>/", ReceptionistDetailView.as_view(), name="receptionist-detail"),
    path("receptionist/me/",       ReceptionistSelfView.as_view(),   name="receptionist-self"),

    # Lab Technicians — admin only
    path("labtechnician/",          LabTechnicianListView.as_view(),   name="lab-list"),
    path("labtechnician/<int:pk>/", LabTechnicianDetailView.as_view(), name="lab-detail"),
    path("labtechnician/me/",       LabTechnicianSelfView.as_view(),   name="lab-self"),

    # Pharmacists — admin only
    path("pharmacist/",          PharmacistListView.as_view(),   name="pharmacist-list"),
    path("pharmacist/<int:pk>/", PharmacistDetailView.as_view(), name="pharmacist-detail"),
    path("pharmacist/me/",       PharmacistSelfView.as_view(),   name="pharmacist-self"),

    # Audit log — admin only
    path("audit/", AuditLogListView.as_view(), name="audit-log"),
]