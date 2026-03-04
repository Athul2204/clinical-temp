from django.contrib import admin
from .models import User, Role, StaffProfile, DoctorProfile, ReceptionistProfile, LabTechnicianProfile, PharmacistProfile, AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'user', 'action', 'timestamp')
    search_fields = ('user__username', 'action', 'description')

@admin.register(LabTechnicianProfile)
class LabTechnicianProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_id', 'user', 'certification')
    search_fields = ('user__username', 'certification')

@admin.register(PharmacistProfile)
class PharmacistProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_id', 'user', 'license_number')
    search_fields = ('user__username', 'license_number')

@admin.register(ReceptionistProfile)
class ReceptionistProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_id', 'user')
    search_fields = ('user__username',)

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'user', 'specialization', 'qualification', 'consultation_fee')
    search_fields = ('user__username', 'specialization')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'name', 'description')

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'user', 'phone', 'salary', 'joining_date')