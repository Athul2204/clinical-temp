# from django.contrib import admin
# from .models import (
#     StaffProfile,
#     DoctorProfile,
#     ReceptionistProfile,
#     LabTechnicianProfile,
#     PharmacistProfile,
#     AuditLog
# )

# # ------------------------------
# # Audit Log Admin
# # ------------------------------
# @admin.register(AuditLog)
# class AuditLogAdmin(admin.ModelAdmin):
#     list_display = ('log_id', 'user', 'module', 'action', 'object_id', 'timestamp')
#     search_fields = ('user__username', 'module', 'action', 'description')
#     list_filter = ('module', 'action', 'timestamp')
#     readonly_fields = ('user', 'module', 'action', 'object_id', 'description', 'timestamp')

#     def has_add_permission(self, request):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False


# # ------------------------------
# # Staff Profile Admin
# # ------------------------------
# @admin.register(StaffProfile)
# class StaffProfileAdmin(admin.ModelAdmin):
#     list_display = (
#         'staff_code',
#         'user',
#         'phone',
#         'role',
#         'qualification',
#         'salary',
#         'joining_date',
#         'is_active'
#     )
#     search_fields = ('staff_code', 'user__username', 'phone', 'qualification')
#     list_filter = ('role', 'is_active', 'joining_date')


# # ------------------------------
# # Doctor Profile Admin
# # ------------------------------
# @admin.register(DoctorProfile)
# class DoctorProfileAdmin(admin.ModelAdmin):
#     list_display = (
#         'doctor_id',
#         'get_staff_code',
#         'get_username',
#         'specialization',
#         'consultation_fee',
#         'experience_years'
#     )
#     search_fields = ('staff__staff_code', 'staff__user__username', 'specialization')

#     def get_staff_code(self, obj):
#         return obj.staff.staff_code
#     get_staff_code.short_description = "Staff Code"

#     def get_username(self, obj):
#         return obj.staff.user.username
#     get_username.short_description = "Username"


# # ------------------------------
# # Receptionist Profile Admin
# # ------------------------------
# @admin.register(ReceptionistProfile)
# class ReceptionistProfileAdmin(admin.ModelAdmin):
#     list_display = ('profile_id', 'get_staff_code', 'get_username')
#     search_fields = ('staff__staff_code', 'staff__user__username')

#     def get_staff_code(self, obj):
#         return obj.staff.staff_code
#     get_staff_code.short_description = "Staff Code"

#     def get_username(self, obj):
#         return obj.staff.user.username
#     get_username.short_description = "Username"


# # ------------------------------
# # Lab Technician Profile Admin
# # ------------------------------
# @admin.register(LabTechnicianProfile)
# class LabTechnicianProfileAdmin(admin.ModelAdmin):
#     list_display = ('profile_id', 'get_staff_code', 'get_username', 'certification_details')
#     search_fields = ('staff__staff_code', 'staff__user__username', 'certification_details')

#     def get_staff_code(self, obj):
#         return obj.staff.staff_code
#     get_staff_code.short_description = "Staff Code"

#     def get_username(self, obj):
#         return obj.staff.user.username
#     get_username.short_description = "Username"


# # ------------------------------
# # Pharmacist Profile Admin
# # ------------------------------
# @admin.register(PharmacistProfile)
# class PharmacistProfileAdmin(admin.ModelAdmin):
#     list_display = ('get_staff_code', 'get_username', 'license_number')
#     search_fields = ('staff__staff_code', 'staff__user__username', 'license_number')

#     def get_staff_code(self, obj):
#         return obj.staff.staff_code
#     get_staff_code.short_description = "Staff Code"

#     def get_username(self, obj):
#         return obj.staff.user.username
#     get_username.short_description = "Username"

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
# 🔥 BASE CLASS (REUSABLE)
# ------------------------------
class RoleBasedStaffAdmin(admin.ModelAdmin):
    role_name = None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "staff" and self.role_name:
            kwargs["queryset"] = StaffProfile.objects.filter(
                role=self.role_name,
                is_active=True
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# ------------------------------
# Staff Profile Admin
# ------------------------------
@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = (
        'staff_code',
        'user',
        'phone',
        'role',
        'qualification',
        'salary',
        'joining_date',
        'is_active'
    )

    search_fields = (
        'staff_code',
        'user__username',
        'phone',
        'qualification'
    )

    list_filter = (
        'role',
        'is_active',
        'joining_date'
    )

    list_editable = ('is_active',)
    ordering = ('-created_at',)


# ------------------------------
# Doctor Profile Admin
# ------------------------------
@admin.register(DoctorProfile)
class DoctorProfileAdmin(RoleBasedStaffAdmin):

    role_name = "Doctor"

    list_display = (
        'doctor_id',
        'get_staff_code',
        'get_username',
        'specialization',
        'consultation_fee',
        'experience_years',
        'is_active_status'
    )

    search_fields = (
        'staff__staff_code',
        'staff__user__username',
        'specialization'
    )

    list_filter = (
        'specialization',
        'staff__is_active'
    )

    def get_staff_code(self, obj):
        return getattr(obj.staff, 'staff_code', 'N/A')
    get_staff_code.short_description = "Staff Code"

    def get_username(self, obj):
        return obj.staff.user.username if obj.staff and obj.staff.user else "N/A"
    get_username.short_description = "Username"

    def is_active_status(self, obj):
        return obj.staff.is_active if obj.staff else False
    is_active_status.boolean = True
    is_active_status.short_description = "Active"


# ------------------------------
# Receptionist Profile Admin
# ------------------------------
@admin.register(ReceptionistProfile)
class ReceptionistProfileAdmin(RoleBasedStaffAdmin):

    role_name = "Receptionist"

    list_display = (
        'profile_id',
        'get_staff_code',
        'get_username',
        'is_active_status'
    )

    search_fields = (
        'staff__staff_code',
        'staff__user__username'
    )

    list_filter = ('staff__is_active',)

    def get_staff_code(self, obj):
        return getattr(obj.staff, 'staff_code', 'N/A')
    get_staff_code.short_description = "Staff Code"

    def get_username(self, obj):
        return obj.staff.user.username if obj.staff and obj.staff.user else "N/A"
    get_username.short_description = "Username"

    def is_active_status(self, obj):
        return obj.staff.is_active if obj.staff else False
    is_active_status.boolean = True
    is_active_status.short_description = "Active"


# ------------------------------
# Lab Technician Profile Admin
# ------------------------------
@admin.register(LabTechnicianProfile)
class LabTechnicianProfileAdmin(RoleBasedStaffAdmin):

    role_name = "Lab Technician"

    list_display = (
        'profile_id',
        'get_staff_code',
        'get_username',
        'certification_details',
        'is_active_status'
    )

    search_fields = (
        'staff__staff_code',
        'staff__user__username',
        'certification_details'
    )

    list_filter = ('staff__is_active',)

    def get_staff_code(self, obj):
        return getattr(obj.staff, 'staff_code', 'N/A')
    get_staff_code.short_description = "Staff Code"

    def get_username(self, obj):
        return obj.staff.user.username if obj.staff and obj.staff.user else "N/A"
    get_username.short_description = "Username"

    def is_active_status(self, obj):
        return obj.staff.is_active if obj.staff else False
    is_active_status.boolean = True
    is_active_status.short_description = "Active"


# ------------------------------
# Pharmacist Profile Admin
# ------------------------------
@admin.register(PharmacistProfile)
class PharmacistProfileAdmin(RoleBasedStaffAdmin):

    role_name = "Pharmacist"

    list_display = (
        'get_staff_code',
        'get_username',
        'license_number',
        'is_active_status'
    )

    search_fields = (
        'staff__staff_code',
        'staff__user__username',
        'license_number'
    )

    list_filter = ('staff__is_active',)

    def get_staff_code(self, obj):
        return getattr(obj.staff, 'staff_code', 'N/A')
    get_staff_code.short_description = "Staff Code"

    def get_username(self, obj):
        return obj.staff.user.username if obj.staff and obj.staff.user else "N/A"
    get_username.short_description = "Username"

    def is_active_status(self, obj):
        return obj.staff.is_active if obj.staff else False
    is_active_status.boolean = True
    is_active_status.short_description = "Active"