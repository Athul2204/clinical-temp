# from django.urls import path
# from .views import (
#     StaffListView, StaffDetailView,
#     DoctorListView, DoctorDetailView,
#     ReceptionistListView, ReceptionistDetailView,
#     LabTechnicianListView, LabTechnicianDetailView,
#     PharmacistListView, PharmacistDetailView,
#     AuditLogListView,
#     AdminDashboardView,
# )

# urlpatterns = [
#     # ─── Dashboard ──────────────────────────────────────────
#     # Method: GET (Summary data)
#     path("dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),

#     # ─── Staff ──────────────────────────────────────────────
#     # URL: /api/administration/staff/ 
#     # Methods: GET (List), POST (Create)
#     path("staff/", StaffListView.as_view(), name="staff-list"),
    
#     # URL: /api/administration/staff/<id>/ 
#     # Methods: GET (Retrieve), PUT (Update), PATCH (Partial), DELETE
#     path("staff/<int:pk>/", StaffDetailView.as_view(), name="staff-detail"),

#     # ─── Doctor ─────────────────────────────────────────────
#     path("doctor/", DoctorListView.as_view(), name="doctor-list"),
#     path("doctor/<int:pk>/", DoctorDetailView.as_view(), name="doctor-detail"),

#     # ─── Receptionist ───────────────────────────────────────
#     path("receptionist/", ReceptionistListView.as_view(), name="receptionist-list"),
#     path("receptionist/<int:pk>/", ReceptionistDetailView.as_view(), name="receptionist-detail"),

#     # ─── Lab Technician ─────────────────────────────────────
#     path("labtechnician/", LabTechnicianListView.as_view(), name="lab-list"),
#     path("labtechnician/<int:pk>/", LabTechnicianDetailView.as_view(), name="lab-detail"),

#     # ─── Pharmacist ─────────────────────────────────────────
#     path("pharmacist/", PharmacistListView.as_view(), name="pharmacist-list"),
#     path("pharmacist/<int:pk>/", PharmacistDetailView.as_view(), name="pharmacist-detail"),

#     # ─── Audit Log ──────────────────────────────────────────
#     # Method: GET (Paginated Logs)
#     path("audit/", AuditLogListView.as_view(), name="audit-log"),
# ]


from django.urls import path
from .views import (
    StaffListView, StaffDetailView,
    DoctorListView, DoctorDetailView,
    ReceptionistListView, ReceptionistDetailView,
    LabTechnicianListView, LabTechnicianDetailView,
    PharmacistListView, PharmacistDetailView,
    AuditLogListView,
    AdminDashboardView,
)

urlpatterns = [
    # ─── Dashboard ──────────────────────────────────────────
    # Method: GET (Summary data)
    path("dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),

    # ─── Staff ──────────────────────────────────────────────
    # URL: /api/administration/staff/ 
    # Methods: GET (List), POST (Create)
    path("staff/", StaffListView.as_view(), name="staff-list"),
    
    # URL: /api/administration/staff/<id>/ 
    # Methods: GET (Retrieve), PUT (Update), PATCH (Partial), DELETE
    path("staff/<int:pk>/", StaffDetailView.as_view(), name="staff-detail"),

    # ─── Doctor ─────────────────────────────────────────────
    path("doctor/", DoctorListView.as_view(), name="doctor-list"),
    path("doctor/<int:pk>/", DoctorDetailView.as_view(), name="doctor-detail"),

    # ─── Receptionist ───────────────────────────────────────
    path("receptionist/", ReceptionistListView.as_view(), name="receptionist-list"),
    path("receptionist/<int:pk>/", ReceptionistDetailView.as_view(), name="receptionist-detail"),

    # ─── Lab Technician ─────────────────────────────────────
    path("labtechnician/", LabTechnicianListView.as_view(), name="lab-list"),
    path("labtechnician/<int:pk>/", LabTechnicianDetailView.as_view(), name="lab-detail"),

    # ─── Pharmacist ─────────────────────────────────────────
    path("pharmacist/", PharmacistListView.as_view(), name="pharmacist-list"),
    path("pharmacist/<int:pk>/", PharmacistDetailView.as_view(), name="pharmacist-detail"),

    # ─── Audit Log ──────────────────────────────────────────
    # Method: GET (Paginated Logs)
    path("audit/", AuditLogListView.as_view(), name="audit-log"),
]
