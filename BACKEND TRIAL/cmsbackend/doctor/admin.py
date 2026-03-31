# from django.contrib import admin
# from .models import Consultation, Prescription, PrescriptionItem, LabTestRequest, LabTestRequestItem

# # ------------------------------
# # Consultation Admin
# # ------------------------------
# @admin.register(Consultation)
# class ConsultationAdmin(admin.ModelAdmin):
#     list_display = ('consultation_code', 'appointment', 'created_at')
#     search_fields = ('consultation_code', 'appointment__patient__first_name', 'appointment__doctor__user__username')
#     list_filter = ('created_at',)

# # ------------------------------
# # Prescription Admin
# # ------------------------------
# @admin.register(Prescription)
# class PrescriptionAdmin(admin.ModelAdmin):
#     list_display = ('prescription_code', 'consultation', 'doctor', 'status', 'created_at', 'sent_at', 'dispensed_at')
#     search_fields = ('prescription_code', 'doctor__user__username', 'consultation__appointment__patient__first_name')
#     list_filter = ('status', 'created_at')

# # ------------------------------
# # Prescription Item Admin
# # ------------------------------
# @admin.register(PrescriptionItem)
# class PrescriptionItemAdmin(admin.ModelAdmin):
#     list_display = ('prescription', 'medicine_name', 'dosage', 'frequency', 'duration')
#     search_fields = ('medicine_name', 'prescription__prescription_code')

# # ------------------------------
# # Lab Test Request Admin
# # ------------------------------
# @admin.register(LabTestRequest)
# class LabTestRequestAdmin(admin.ModelAdmin):
#     list_display = ('id', 'consultation', 'doctor', 'status', 'created_at', 'completed_at')
#     search_fields = ('consultation__consultation_code', 'doctor__user__username')
#     list_filter = ('status', 'created_at')

# # ------------------------------
# # Lab Test Request Item Admin
# # ------------------------------
# @admin.register(LabTestRequestItem)
# class LabTestRequestItemAdmin(admin.ModelAdmin):
#     list_display = ('lab_request', 'lab_test')
#     search_fields = ('lab_test__test_name', 'lab_request__consultation__consultation_code')

from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import (
    Consultation,
    Prescription,
    PrescriptionItem,
    LabTestRequest,
    LabTestRequestItem
)


# ------------------------------
# INLINE: Prescription Items
# ------------------------------
class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1


# ------------------------------
# INLINE: Lab Test Items
# ------------------------------
class LabTestRequestItemInline(admin.TabularInline):
    model = LabTestRequestItem
    extra = 1


# ------------------------------
# Consultation Admin
# ------------------------------
@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):

    list_display = (
        'consultation_code',
        'get_patient',
        'get_doctor',
        'get_token',
        'created_at'
    )

    search_fields = (
        'consultation_code',
        'appointment__patient__first_name',
        'appointment__patient__last_name',
        'appointment__doctor__staff__user__username'
    )

    list_filter = ('created_at',)

    readonly_fields = ('consultation_code', 'created_at')

    # ------------------------------
    # SAFE DISPLAY METHODS
    # ------------------------------
    def get_patient(self, obj):
        return getattr(obj.appointment, "patient", "N/A")
    get_patient.short_description = "Patient"

    def get_doctor(self, obj):
        if obj.appointment and obj.appointment.doctor and obj.appointment.doctor.staff:
            return obj.appointment.doctor.staff.user.username
        return "N/A"
    get_doctor.short_description = "Doctor"

    def get_token(self, obj):
        return getattr(obj.appointment, "token_number", "N/A")
    get_token.short_description = "Token"


# ------------------------------
# Prescription Admin
# ------------------------------
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):

    inlines = [PrescriptionItemInline]

    list_display = (
        'prescription_code',
        'get_patient',
        'get_doctor',
        'status',
        'created_at',
        'sent_at',
        'dispensed_at'
    )

    search_fields = (
        'prescription_code',
        'consultation__appointment__patient__first_name',
        'consultation__appointment__doctor__staff__user__username'
    )

    list_filter = ('status', 'created_at')

    readonly_fields = ('prescription_code', 'created_at', 'sent_at', 'dispensed_at')

    actions = ['send_to_pharmacy_action']

    # ------------------------------
    # SAFE DISPLAY METHODS
    # ------------------------------
    def get_patient(self, obj):
        if obj.consultation and obj.consultation.appointment:
            return obj.consultation.appointment.patient
        return "N/A"
    get_patient.short_description = "Patient"

    def get_doctor(self, obj):
        if obj.doctor and obj.doctor.staff:
            return obj.doctor.staff.user.username
        return "N/A"
    get_doctor.short_description = "Doctor"

    # ------------------------------
    # ADMIN ACTION
    # ------------------------------
    def send_to_pharmacy_action(self, request, queryset):
        success = 0
        for obj in queryset:
            try:
                obj.send_to_pharmacy()
                success += 1
            except ValidationError as e:
                self.message_user(request, f"{obj}: {e}", level="error")

        self.message_user(request, f"{success} prescriptions sent successfully")

    send_to_pharmacy_action.short_description = "Send selected to Pharmacy"


# ------------------------------
# Prescription Item Admin
# ------------------------------
@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):

    list_display = (
        'prescription',
        'medicine_name',
        'dosage',
        'frequency',
        'duration'
    )

    search_fields = (
        'medicine_name__name',
        'prescription__prescription_code'
    )


# ------------------------------
# Lab Test Request Admin
# ------------------------------
@admin.register(LabTestRequest)
class LabTestRequestAdmin(admin.ModelAdmin):

    inlines = [LabTestRequestItemInline]

    list_display = (
        'id',
        'get_patient',
        'get_doctor',
        'status',
        'get_result_count',   # 🔥 NEW FEATURE
        'created_at',
        'completed_at'
    )

    search_fields = (
        'consultation__consultation_code',
        'consultation__appointment__patient__first_name',
        'doctor__staff__user__username'
    )

    list_filter = ('status', 'created_at')

    readonly_fields = ('created_at', 'completed_at')

    # ------------------------------
    # SAFE DISPLAY METHODS
    # ------------------------------
    def get_patient(self, obj):
        if obj.consultation and obj.consultation.appointment:
            return obj.consultation.appointment.patient
        return "N/A"
    get_patient.short_description = "Patient"

    def get_doctor(self, obj):
        if obj.doctor and obj.doctor.staff:
            return obj.doctor.staff.user.username
        return "N/A"
    get_doctor.short_description = "Doctor"

    # 🔥 SHOW RESULT COUNT (VERY IMPORTANT UX)
    def get_result_count(self, obj):
        try:
            return obj.get_lab_results().count()
        except:
            return 0
    get_result_count.short_description = "Results"


# ------------------------------
# Lab Test Request Item Admin
# ------------------------------
@admin.register(LabTestRequestItem)
class LabTestRequestItemAdmin(admin.ModelAdmin):

    list_display = (
        'lab_request',
        'lab_test'
    )

    search_fields = (
        'lab_test__test_name',
        'lab_request__consultation__consultation_code'
    )