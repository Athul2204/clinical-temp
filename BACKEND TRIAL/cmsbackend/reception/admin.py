# from django.contrib import admin
# from django import forms
# from .models import Patient, DoctorAvailability, Appointment, ConsultationBill


# # ------------------------------
# # Patient Admin Form (Phone only numbers)
# # ------------------------------
# class PatientAdminForm(forms.ModelForm):

#     class Meta:
#         model = Patient
#         fields = "__all__"

#     phone = forms.CharField(
#         max_length=10,
#         widget=forms.TextInput(attrs={
#             "type": "tel",
#             "maxlength": "10",
#             "pattern": "[0-9]{10}",
#             "inputmode": "numeric",
#             "oninput": "this.value = this.value.replace(/[^0-9]/g, '')"
#         })
#     )


# # ------------------------------
# # Patient Admin
# # ------------------------------
# @admin.register(Patient)
# class PatientAdmin(admin.ModelAdmin):

#     form = PatientAdminForm

#     list_display = (
#         'patient_id',
#         'first_name',
#         'last_name',
#         'email',
#         'phone',
#         'gender',
#         'membership_status',
#         'age'
#     )

#     search_fields = (
#         'first_name',
#         'last_name',
#         'email',
#         'phone'
#     )

#     list_filter = (
#         'gender',
#         'membership_status'
#     )


# # ------------------------------
# # Doctor Availability Admin
# # ------------------------------
# @admin.register(DoctorAvailability)
# class DoctorAvailabilityAdmin(admin.ModelAdmin):

#     list_display = (
#         'availability_id',
#         'doctor',
#         'available_date',
#         'start_time',
#         'end_time'
#     )

#     search_fields = (
#         'doctor__user__username',
#     )

#     list_filter = (
#         'available_date',
#     )


# # ------------------------------
# # Appointment Admin
# # ------------------------------
# @admin.register(Appointment)
# class AppointmentAdmin(admin.ModelAdmin):

#     list_display = (
#         'appointment_id',
#         'patient',
#         'doctor',
#         'appointment_date',
#         'appointment_time',
#         'status'
#     )

#     search_fields = (
#         'patient__first_name',
#         'patient__last_name',
#         'doctor__user__username'
#     )

#     list_filter = (
#         'status',
#         'appointment_date'
#     )


# # ------------------------------
# # Consultation Billing Admin
# # ------------------------------
# @admin.register(ConsultationBill)
# class ConsultationBillAdmin(admin.ModelAdmin):

#     list_display = (
#         'bill_id',
#         'appointment',
#         'amount',
#         'status',
#         'created_at'
#     )

#     search_fields = (
#         'appointment__patient__first_name',
#         'appointment__doctor__user__username'
#     )

#     list_filter = (
#         'status',
#         'created_at'
#     )

from django.contrib import admin
from django import forms
from .models import Patient, DoctorAvailability, Appointment, ConsultationBill
from administration.models import DoctorProfile


# ------------------------------
# COMMON FUNCTION (REUSE)
# ------------------------------
def format_doctor(obj):
    if obj and obj.staff and obj.staff.user:
        return f"{obj.staff.staff_code} | {obj.staff.user.username} | {obj.specialization}"
    return "N/A"


# ------------------------------
# Patient Admin Form
# ------------------------------
class PatientAdminForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = "__all__"

    phone = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            "type": "tel",
            "maxlength": "10",
            "pattern": "[0-9]{10}",
            "inputmode": "numeric",
            "oninput": "this.value = this.value.replace(/[^0-9]/g, '')"
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

    ordering = ('-created_at',)


# ------------------------------
# Doctor Availability Form
# ------------------------------
class DoctorAvailabilityAdminForm(forms.ModelForm):

    class Meta:
        model = DoctorAvailability
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['doctor'].queryset = DoctorProfile.objects.select_related(
            'staff__user'
        ).filter(staff__is_active=True)

        self.fields['doctor'].label_from_instance = lambda obj: format_doctor(obj)


# ------------------------------
# Doctor Availability Admin
# ------------------------------
@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):

    form = DoctorAvailabilityAdminForm

    list_display = (
        'availability_id',
        'doctor_info',
        'available_date',
        'start_time',
        'end_time'
    )

    search_fields = (
        'doctor__staff__user__username',
    )

    list_filter = (
        'available_date',
    )

    def doctor_info(self, obj):
        return format_doctor(obj.doctor)
    doctor_info.short_description = "Doctor"


# ------------------------------
# Appointment Form
# ------------------------------
class AppointmentAdminForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['doctor'].queryset = DoctorProfile.objects.select_related(
            'staff__user'
        ).filter(staff__is_active=True)

        self.fields['doctor'].label_from_instance = lambda obj: format_doctor(obj)


# ------------------------------
# Appointment Admin
# ------------------------------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    form = AppointmentAdminForm

    list_display = (
        'appointment_id',
        'patient',
        'doctor_info',
        'appointment_date',
        'appointment_time',
        'token_number',          # 🔥 IMPORTANT
        'consultation_fee',
        'status'
    )

    search_fields = (
        'patient__first_name',
        'patient__last_name',
        'doctor__staff__user__username'
    )

    list_filter = (
        'status',
        'appointment_date'
    )

    ordering = ('-appointment_date', 'token_number')

    def doctor_info(self, obj):
        return format_doctor(obj.doctor)
    doctor_info.short_description = "Doctor"


# ------------------------------
# Consultation Bill Admin
# ------------------------------
@admin.register(ConsultationBill)
class ConsultationBillAdmin(admin.ModelAdmin):

    list_display = (
        'bill_id',
        'get_patient',
        'get_doctor',
        'amount',
        'status',
        'created_at'
    )

    search_fields = (
        'appointment__patient__first_name',
        'appointment__doctor__staff__user__username'
    )

    list_filter = (
        'status',
        'created_at'
    )

    ordering = ('-created_at',)

    def get_patient(self, obj):
        return obj.appointment.patient
    get_patient.short_description = "Patient"

    def get_doctor(self, obj):
        return format_doctor(obj.appointment.doctor)
    get_doctor.short_description = "Doctor"