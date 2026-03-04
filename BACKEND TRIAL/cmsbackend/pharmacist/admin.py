from django.contrib import admin
from .models import Medicine, MedicineBatch, MedicineStockLog, Dispense, DispenseItem, MedicineBill

# ------------------------------
# Medicine Admin
# ------------------------------
@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('medicine_id', 'name', 'unit', 'price')
    search_fields = ('name',)

# ------------------------------
# Medicine Batch Admin
# ------------------------------
@admin.register(MedicineBatch)
class MedicineBatchAdmin(admin.ModelAdmin):
    list_display = ('batch_id', 'medicine', 'batch_number', 'quantity', 'expiry_date')
    search_fields = ('medicine__name', 'batch_number')
    list_filter = ('expiry_date',)

# ------------------------------
# Medicine Stock Log Admin
# ------------------------------
@admin.register(MedicineStockLog)
class MedicineStockLogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'batch', 'change_type', 'quantity_changed', 'created_at')
    search_fields = ('batch__batch_number', 'batch__medicine__name')
    list_filter = ('change_type', 'created_at')

# ------------------------------
# Dispense Admin
# ------------------------------
@admin.register(Dispense)
class DispenseAdmin(admin.ModelAdmin):
    list_display = ('dispense_id', 'prescription', 'patient', 'total_amount', 'status', 'dispense_date')
    search_fields = ('prescription__prescription_code', 'patient__first_name', 'patient__last_name')
    list_filter = ('status', 'dispense_date')

# ------------------------------
# Dispense Item Admin
# ------------------------------
@admin.register(DispenseItem)
class DispenseItemAdmin(admin.ModelAdmin):
    list_display = ('dispense', 'batch', 'quantity', 'price')
    search_fields = ('batch__batch_number', 'batch__medicine__name')

# ------------------------------
# Medicine Bill Admin
# ------------------------------
@admin.register(MedicineBill)
class MedicineBillAdmin(admin.ModelAdmin):
    list_display = ('bill_id', 'dispense', 'total_amount', 'discount', 'final_amount', 'payment_status', 'created_at')
    search_fields = ('dispense__dispense_id', 'dispense__patient__first_name')
    list_filter = ('payment_status', 'created_at')