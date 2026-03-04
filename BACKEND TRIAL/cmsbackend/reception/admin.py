from django.contrib import admin
from .models import Patient, Appointment, ConsultationBill, DoctorAvailability

# ------------------------------
# Patient Admin
# ------------------------------
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'first_name', 'last_name', 'phone', 'email', 'gender', 'membership_status', 'age', 'created_at')

# ------------------------------
# Appointment Admin
# ------------------------------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'token_number', 'created_at')

# ------------------------------
# ConsultationBill Admin
# ------------------------------
@admin.register(ConsultationBill)
class ConsultationBillAdmin(admin.ModelAdmin):
    # Match field names from models
    list_display = ('bill_id', 'appointment', 'amount', 'status', 'created_at')

# ------------------------------
# DoctorAvailability Admin
# ------------------------------
@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('availability_id', 'doctor', 'available_date', 'start_time', 'end_time')