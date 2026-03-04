from django.contrib import admin
from .models import LabTest, LabOrder, LabOrderItem, LabResult, LabBill, LabEquipment, LabMaintenance

# ------------------------------
# LabTest Admin
# ------------------------------
@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('test_id', 'test_name', 'cost', 'unit')

# ------------------------------
# LabOrder Admin
# ------------------------------
@admin.register(LabOrder)
class LabOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_number', 'lab_request', 'patient', 'status', 'created_at')

# ------------------------------
# LabOrderItem Admin
# ------------------------------
@admin.register(LabOrderItem)
class LabOrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_item_id', 'lab_order', 'lab_test')

# ------------------------------
# LabResult Admin
# ------------------------------
@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ('result_id', 'lab_order_item', 'result_value', 'is_critical', 'created_at')

# ------------------------------
# LabBill Admin
# ------------------------------
@admin.register(LabBill)
class LabBillAdmin(admin.ModelAdmin):
    list_display = ('lab_bill_id', 'bill_number', 'lab_order', 'total_amount', 'final_amount', 'payment_status', 'created_at')

# ------------------------------
# LabEquipment Admin
# ------------------------------
@admin.register(LabEquipment)
class LabEquipmentAdmin(admin.ModelAdmin):
    list_display = ('equipment_id', 'name', 'purchase_date', 'last_service_date', 'status')

# ------------------------------
# LabMaintenance Admin
# ------------------------------
@admin.register(LabMaintenance)
class LabMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('maintenance_id', 'equipment', 'service_date', 'technician_name', 'cost')