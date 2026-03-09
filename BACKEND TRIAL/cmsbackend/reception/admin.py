from django.contrib import admin
from django import forms
from .models import Patient, DoctorAvailability, Appointment, ConsultationBill


# ------------------------------
# Patient Admin Form (Phone only numbers)
# ------------------------------
class PatientAdminForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = "__all__"

    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            "pattern": "[0-9]*",
            "inputmode": "numeric",
        })
    )


# ------------------------------
# Patient Admin
# ------------------------------
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):

    form = PatientAdminForm

    list_display = (
        'patient_id',
        'first_name',
        'last_name',
        'email',
        'phone',
        'gender',
        'membership_status',
        'age'
    )

    search_fields = (
        'first_name',
        'last_name',
        'email',
        'phone'
    )

    list_filter = (
        'gender',
        'membership_status'
    )


# ------------------------------
# Doctor Availability Admin
# ------------------------------
@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):

    list_display = (
        'availability_id',
        'doctor',
        'available_date',
        'start_time',
        'end_time'
    )

    search_fields = (
        'doctor__user__username',
    )

    list_filter = (
        'available_date',
    )


# ------------------------------
# Appointment Admin
# ------------------------------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        'appointment_id',
        'patient',
        'doctor',
        'appointment_date',
        'appointment_time',
        'status'
    )

    search_fields = (
        'patient__first_name',
        'patient__last_name',
        'doctor__user__username'
    )

    list_filter = (
        'status',
        'appointment_date'
    )


# ------------------------------
# Consultation Billing Admin
# ------------------------------
@admin.register(ConsultationBill)
class ConsultationBillAdmin(admin.ModelAdmin):

    list_display = (
        'bill_id',
        'appointment',
        'amount',
        'status',
        'created_at'
    )

    search_fields = (
        'appointment__patient__first_name',
        'appointment__doctor__user__username'
    )

    list_filter = (
        'status',
        'created_at'
    )