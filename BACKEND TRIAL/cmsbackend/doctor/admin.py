from django.contrib import admin
from .models import Consultation, Prescription, PrescriptionItem, LabTestRequest, LabTestRequestItem

# ------------------------------
# Consultation Admin
# ------------------------------
@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('consultation_code', 'appointment', 'created_at')
    search_fields = ('consultation_code', 'appointment__patient__first_name', 'appointment__doctor__user__username')
    list_filter = ('created_at',)

# ------------------------------
# Prescription Admin
# ------------------------------
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_code', 'consultation', 'doctor', 'status', 'created_at', 'sent_at', 'dispensed_at')
    search_fields = ('prescription_code', 'doctor__user__username', 'consultation__appointment__patient__first_name')
    list_filter = ('status', 'created_at')

# ------------------------------
# Prescription Item Admin
# ------------------------------
@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ('prescription', 'medicine_name', 'dosage', 'frequency', 'duration')
    search_fields = ('medicine_name', 'prescription__prescription_code')

# ------------------------------
# Lab Test Request Admin
# ------------------------------
@admin.register(LabTestRequest)
class LabTestRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'consultation', 'doctor', 'status', 'created_at', 'completed_at')
    search_fields = ('consultation__consultation_code', 'doctor__user__username')
    list_filter = ('status', 'created_at')

# ------------------------------
# Lab Test Request Item Admin
# ------------------------------
@admin.register(LabTestRequestItem)
class LabTestRequestItemAdmin(admin.ModelAdmin):
    list_display = ('lab_request', 'lab_test')
    search_fields = ('lab_test__test_name', 'lab_request__consultation__consultation_code')