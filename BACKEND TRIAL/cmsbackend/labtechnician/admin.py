# from django.contrib import admin
# from .models import LabTest, LabOrder, LabOrderItem, LabResult, LabBill, LabEquipment, LabMaintenance

# # ------------------------------
# # Lab Test Admin
# # ------------------------------
# @admin.register(LabTest)
# class LabTestAdmin(admin.ModelAdmin):
#     list_display = ('test_id', 'test_name', 'cost', 'unit', 'normal_range')
#     search_fields = ('test_name',)

# # ------------------------------
# # Lab Order Admin
# # ------------------------------
# @admin.register(LabOrder)
# class LabOrderAdmin(admin.ModelAdmin):
#     list_display = ('order_id', 'order_number', 'lab_request', 'patient', 'status', 'created_at')
#     search_fields = ('order_number', 'patient__first_name', 'lab_request__consultation__consultation_code')
#     list_filter = ('status', 'created_at')

# # ------------------------------
# # Lab Order Item Admin
# # ------------------------------
# @admin.register(LabOrderItem)
# class LabOrderItemAdmin(admin.ModelAdmin):
#     list_display = ('lab_order', 'lab_test')
#     search_fields = ('lab_test__test_name', 'lab_order__order_number')

# # ------------------------------
# # Lab Result Admin
# # ------------------------------
# @admin.register(LabResult)
# class LabResultAdmin(admin.ModelAdmin):
#     list_display = ('result_id', 'lab_order_item', 'result_value', 'is_critical', 'created_at')
#     search_fields = ('lab_order_item__lab_test__test_name',)
#     list_filter = ('is_critical', 'created_at')

# # ------------------------------
# # Lab Bill Admin
# # ------------------------------
# @admin.register(LabBill)
# class LabBillAdmin(admin.ModelAdmin):
#     list_display = ('lab_bill_id', 'bill_number', 'lab_order', 'total_amount', 'discount', 'final_amount', 'payment_status', 'created_at')
#     search_fields = ('bill_number', 'lab_order__order_number')
#     list_filter = ('payment_status', 'created_at')

# # ------------------------------
# # Lab Equipment Admin
# # ------------------------------
# @admin.register(LabEquipment)
# class LabEquipmentAdmin(admin.ModelAdmin):
#     list_display = ('equipment_id', 'name', 'purchase_date', 'last_service_date', 'status')
#     search_fields = ('name',)
#     list_filter = ('status',)

# # ------------------------------
# # Lab Maintenance Admin
# # ------------------------------
# @admin.register(LabMaintenance)
# class LabMaintenanceAdmin(admin.ModelAdmin):
#     list_display = ('maintenance_id', 'equipment', 'service_date', 'technician_name', 'cost')
#     search_fields = ('equipment__name', 'technician_name')
#     list_filter = ('service_date',)

from django.contrib import admin
from .models import (
    LabTest,
    LabOrder,
    LabOrderItem,
    LabResult,
    LabBill,
    LabEquipment,
    LabMaintenance
)


# ------------------------------
# Lab Test Admin
# ------------------------------
@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('test_id', 'test_name', 'cost', 'unit', 'normal_range')
    search_fields = ('test_name',)


# ------------------------------
# Lab Order Admin
# ------------------------------
@admin.register(LabOrder)
class LabOrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'order_number',
        'get_patient',
        'get_doctor',
        'status',
        'created_at'
    )

    search_fields = (
        'order_number',
        'patient__first_name',
        'lab_request__consultation__consultation_code',
        'lab_request__doctor__staff__user__username'
    )

    list_filter = ('status', 'created_at')

    # ✅ SAFE DISPLAY METHODS
    def get_patient(self, obj):
        return obj.patient
    get_patient.short_description = "Patient"

    def get_doctor(self, obj):
        try:
            return obj.lab_request.doctor.staff.user.username
        except:
            return "N/A"
    get_doctor.short_description = "Doctor"


# ------------------------------
# Lab Order Item Admin
# ------------------------------
@admin.register(LabOrderItem)
class LabOrderItemAdmin(admin.ModelAdmin):
    list_display = ('lab_order', 'lab_test')
    search_fields = ('lab_test__test_name', 'lab_order__order_number')


# ------------------------------
# Lab Result Admin
# ------------------------------
@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = (
        'result_id',
        'get_test',
        'get_order',
        'result_value',
        'is_critical',
        'created_at'
    )

    search_fields = (
        'lab_order_item__lab_test__test_name',
        'lab_order_item__lab_order__order_number'
    )

    list_filter = ('is_critical', 'created_at')

    def get_test(self, obj):
        return obj.lab_order_item.lab_test.test_name
    get_test.short_description = "Test"

    def get_order(self, obj):
        return obj.lab_order_item.lab_order.order_number
    get_order.short_description = "Order"


# ------------------------------
# Lab Bill Admin
# ------------------------------
@admin.register(LabBill)
class LabBillAdmin(admin.ModelAdmin):
    list_display = (
        'lab_bill_id',
        'bill_number',
        'get_patient',
        'total_amount',
        'discount',
        'final_amount',
        'payment_status',
        'created_at'
    )

    search_fields = (
        'bill_number',
        'lab_order__order_number',
        'lab_order__patient__first_name'
    )

    list_filter = ('payment_status', 'created_at')

    def get_patient(self, obj):
        return obj.lab_order.patient
    get_patient.short_description = "Patient"


# ------------------------------
# Lab Equipment Admin
# ------------------------------
@admin.register(LabEquipment)
class LabEquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'equipment_id',
        'name',
        'purchase_date',
        'last_service_date',
        'status'
    )

    search_fields = ('name',)
    list_filter = ('status',)


# ------------------------------
# Lab Maintenance Admin
# ------------------------------
@admin.register(LabMaintenance)
class LabMaintenanceAdmin(admin.ModelAdmin):
    list_display = (
        'maintenance_id',
        'equipment',
        'service_date',
        'technician_name',
        'cost'
    )

    search_fields = ('equipment__name', 'technician_name')
    list_filter = ('service_date',)