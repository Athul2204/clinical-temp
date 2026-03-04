from django.contrib import admin
from .models import (
    StaffProfile,
    DoctorProfile,
    ReceptionistProfile,
    LabTechnicianProfile,
    PharmacistProfile,
    AuditLog
)


# ------------------------------
# Audit Log Admin
# ------------------------------
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'user', 'module', 'action', 'object_id', 'timestamp')
    search_fields = ('user__username', 'module', 'action', 'description')
    list_filter = ('module', 'action', 'timestamp')
    readonly_fields = ('user', 'module', 'action', 'object_id', 'description', 'timestamp')

    def has_add_permission(self, request):
        return False  # prevent manual creation

    def has_delete_permission(self, request, obj=None):
        return False  # prevent deletion


# ------------------------------
# Staff Profile Admin
# ------------------------------
@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'staff_code',
        'user',
        'phone',
        'qualification',
        'salary',
        'joining_date',
        'is_active'
    )
    search_fields = ('staff_code', 'user__username', 'phone', 'qualification')
    list_filter = ('is_active', 'joining_date')


# ------------------------------
# Doctor Profile Admin
# ------------------------------
@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = (
        'doctor_id',
        'get_staff_code',
        'get_username',
        'specialization',
        'consultation_fee',
        'experience_years'
    )
    search_fields = ('staff__staff_code', 'staff__user__username', 'specialization')

    def get_staff_code(self, obj):
        return obj.staff.staff_code
    get_staff_code.short_description = "Staff Code"

    def get_username(self, obj):
        return obj.staff.user.username
    get_username.short_description = "Username"


# ------------------------------
# Receptionist Admin
# ------------------------------
@admin.register(ReceptionistProfile)
class ReceptionistProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_id', 'get_staff_code', 'get_username')
    search_fields = ('staff__staff_code', 'staff__user__username')

    def get_staff_code(self, obj):
        return obj.staff.staff_code
    get_staff_code.short_description = "Staff Code"

    def get_username(self, obj):
        return obj.staff.user.username
    get_username.short_description = "Username"


# ------------------------------
# Lab Technician Admin
# ------------------------------
@admin.register(LabTechnicianProfile)
class LabTechnicianProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_id', 'get_staff_code', 'get_username', 'certification_details')
    search_fields = ('staff__staff_code', 'staff__user__username', 'certification_details')

    def get_staff_code(self, obj):
        return obj.staff.staff_code
    get_staff_code.short_description = "Staff Code"

    def get_username(self, obj):
        return obj.staff.user.username
    get_username.short_description = "Username"


# ------------------------------
# Pharmacist Admin
# ------------------------------
@admin.register(PharmacistProfile)
class PharmacistProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_id', 'get_staff_code', 'get_username', 'license_number')
    search_fields = ('staff__staff_code', 'staff__user__username', 'license_number')

    def get_staff_code(self, obj):
        return obj.staff.staff_code
    get_staff_code.short_description = "Staff Code"

    def get_username(self, obj):
        return obj.staff.user.username
    get_username.short_description = "Username"