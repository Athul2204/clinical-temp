from django.contrib import admin
from .models import Medicine, MedicineBatch, MedicineStockLog, Dispense, DispenseItem, MedicineBill

# ------------------------------
# Medicine Admin
# ------------------------------
@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('medicine_id', 'name', 'unit', 'price')

# ------------------------------
# MedicineBatch Admin
# ------------------------------
@admin.register(MedicineBatch)
class MedicineBatchAdmin(admin.ModelAdmin):
    list_display = ('batch_id', 'medicine', 'batch_number', 'quantity', 'expiry_date', 'created_at')

# ------------------------------
# MedicineStockLog Admin
# ------------------------------
@admin.register(MedicineStockLog)
class MedicineStockLogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'batch', 'change_type', 'quantity_changed', 'created_at')

# ------------------------------
# Dispense Admin
# ------------------------------
@admin.register(Dispense)
class DispenseAdmin(admin.ModelAdmin):
    list_display = ('dispense_id', 'prescription', 'patient', 'total_amount', 'status', 'dispense_date')

# ------------------------------
# DispenseItem Admin
# ------------------------------
@admin.register(DispenseItem)
class DispenseItemAdmin(admin.ModelAdmin):
    list_display = ('dispense_item_id', 'dispense', 'batch', 'quantity', 'price')

# ------------------------------
# MedicineBill Admin
# ------------------------------
@admin.register(MedicineBill)
class MedicineBillAdmin(admin.ModelAdmin):
    list_display = ('bill_id', 'dispense', 'total_amount', 'discount', 'final_amount', 'payment_status', 'created_at')