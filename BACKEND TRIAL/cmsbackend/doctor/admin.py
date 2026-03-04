from django.contrib import admin
from .models import Consultation, Prescription, PrescriptionItem, LabTestRequest, LabTestRequestItem

# ------------------------------
# Consultation Admin
# ------------------------------
@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('consultation_code', 'appointment', 'created_at')

# ------------------------------
# LabTestRequest Admin
# ------------------------------
@admin.register(LabTestRequest)
class LabTestRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'consultation', 'doctor', 'status', 'created_at', 'completed_at')

# ------------------------------
# LabTestRequestItem Admin
# ------------------------------
@admin.register(LabTestRequestItem)
class LabTestRequestItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'lab_request', 'lab_test')

# ------------------------------
# Prescription Admin
# ------------------------------
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_code', 'consultation', 'doctor', 'status', 'created_at', 'sent_at', 'dispensed_at')

# ------------------------------
# PrescriptionItem Admin
# ------------------------------
@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'prescription', 'medicine_name', 'dosage', 'frequency', 'duration')