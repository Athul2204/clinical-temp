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

    # FIX 4: /me/ routes MUST come before /<int:pk>/ routes.
    # Django matches URL patterns top-to-bottom. If /<int:pk>/ is listed
    # first, the string "me" fails the int cast → 404 instead of routing
    # to the self-profile view. Placing /me/ first fixes this.

    # Doctors — GET: any authenticated | write: admin only
    path("doctor/me/",       DoctorSelfView.as_view(),   name="doctor-self"),
    path("doctor/",          DoctorListView.as_view(),   name="doctor-list"),
    path("doctor/<int:pk>/", DoctorDetailView.as_view(), name="doctor-detail"),

    # Receptionists — admin only (self-read for receptionists)
    path("receptionist/me/",       ReceptionistSelfView.as_view(),   name="receptionist-self"),
    path("receptionist/",          ReceptionistListView.as_view(),   name="receptionist-list"),
    path("receptionist/<int:pk>/", ReceptionistDetailView.as_view(), name="receptionist-detail"),

    # Lab Technicians — admin only (self-read for lab techs)
    path("labtechnician/me/",       LabTechnicianSelfView.as_view(),   name="lab-self"),
    path("labtechnician/",          LabTechnicianListView.as_view(),   name="lab-list"),
    path("labtechnician/<int:pk>/", LabTechnicianDetailView.as_view(), name="lab-detail"),

    # Pharmacists — admin only (self-read for pharmacists)
    path("pharmacist/me/",       PharmacistSelfView.as_view(),   name="pharmacist-self"),
    path("pharmacist/",          PharmacistListView.as_view(),   name="pharmacist-list"),
    path("pharmacist/<int:pk>/", PharmacistDetailView.as_view(), name="pharmacist-detail"),

    # Audit log — admin only
    path("audit/", AuditLogListView.as_view(), name="audit-log"),
]