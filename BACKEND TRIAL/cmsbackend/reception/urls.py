# from django.urls import path
# from .views import (
#     CreatePatientView,
#     PatientListView,
#     CreateAppointmentView,
#     AppointmentListByDateView,
#     CancelAppointmentView,
#     CreateBillView,
#     PayBillView
# )

# urlpatterns = [

#     # Patients
#     path('patients/create/', CreatePatientView.as_view()),
#     path('patients/', PatientListView.as_view()),

#     # Appointments
#     path('appointments/create/', CreateAppointmentView.as_view()),
#     path('appointments-by-date/', AppointmentListByDateView.as_view()),
#     path('appointments/<int:appointment_id>/cancel/', CancelAppointmentView.as_view()),

#     # Bills
#     path('bills/create/', CreateBillView.as_view()),
#     path('bills/<int:bill_id>/pay/', PayBillView.as_view()),
# ]


from django.urls import path
from .views import (
    CreatePatientView,
    PatientListView,
    CreateAppointmentView,
    AppointmentListByDateView,
    CancelAppointmentView,
    CreateBillView,
    PayBillView,
    DoctorAvailabilityListView,
    CreateDoctorAvailabilityView,
    DeleteDoctorAvailabilityView,
)

urlpatterns = [

    # Patients
    path('patients/create/', CreatePatientView.as_view()),
    path('patients/', PatientListView.as_view()),

    # Appointments
    path('appointments/create/', CreateAppointmentView.as_view()),
    path('appointments-by-date/', AppointmentListByDateView.as_view()),
    path('appointments/<int:appointment_id>/cancel/', CancelAppointmentView.as_view()),

    # Bills
    path('bills/create/', CreateBillView.as_view()),
    path('bills/<int:bill_id>/pay/', PayBillView.as_view()),

    # Doctor Availability
    path('availability/', DoctorAvailabilityListView.as_view()),
    path('availability/create/', CreateDoctorAvailabilityView.as_view()),
    path('availability/<int:availability_id>/delete/', DeleteDoctorAvailabilityView.as_view()),
]