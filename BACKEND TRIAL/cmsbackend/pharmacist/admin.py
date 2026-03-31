# from django.contrib import admin
# from .models import Medicine, MedicineBatch, MedicineStockLog, Dispense, DispenseItem, MedicineBill

# # ------------------------------
# # Medicine Admin
# # ------------------------------
# @admin.register(Medicine)
# class MedicineAdmin(admin.ModelAdmin):
#     list_display = ('medicine_id', 'name', 'unit', 'price')
#     search_fields = ('name',)

# # ------------------------------
# # Medicine Batch Admin
# # ------------------------------
# @admin.register(MedicineBatch)
# class MedicineBatchAdmin(admin.ModelAdmin):
#     list_display = ('batch_id', 'medicine', 'batch_number', 'quantity', 'expiry_date')
#     search_fields = ('medicine__name', 'batch_number')
#     list_filter = ('expiry_date',)

# # ------------------------------
# # Medicine Stock Log Admin
# # ------------------------------
# @admin.register(MedicineStockLog)
# class MedicineStockLogAdmin(admin.ModelAdmin):
#     list_display = ('log_id', 'batch', 'change_type', 'quantity_changed', 'created_at')
#     search_fields = ('batch__batch_number', 'batch__medicine__name')
#     list_filter = ('change_type', 'created_at')

# # ------------------------------
# # Dispense Admin
# # ------------------------------
# @admin.register(Dispense)
# class DispenseAdmin(admin.ModelAdmin):
#     list_display = ('dispense_id', 'prescription', 'patient', 'total_amount', 'status', 'dispense_date')
#     search_fields = ('prescription__prescription_code', 'patient__first_name', 'patient__last_name')
#     list_filter = ('status', 'dispense_date')

# # ------------------------------
# # Dispense Item Admin
# # -------------------------A-----
# @admin.register(DispenseItem)
# class DispenseItemAdmin(admin.ModelAdmin):
#     list_display = ('dispense', 'batch', 'quantity', 'price')
#     search_fields = ('batch__batch_number', 'batch__medicine__name')

# # ------------------------------
# # Medicine Bill Admin
# # ------------------------------
# @admin.register(MedicineBill)
# class MedicineBillAdmin(admin.ModelAdmin):
#     list_display = ('bill_id', 'dispense', 'total_amount', 'discount', 'final_amount', 'payment_status', 'created_at')
#     search_fields = ('dispense__dispense_id', 'dispense__patient__first_name')
#     list_filter = ('payment_status', 'created_at')


from django.contrib import admin
from django.utils import timezone
from .models import (
    Medicine,
    MedicineBatch,
    MedicineStockLog,
    Dispense,
    DispenseItem,
    MedicineBill
)


# ------------------------------
# INLINE: Dispense Items
# ------------------------------
class DispenseItemInline(admin.TabularInline):
    model = DispenseItem
    extra = 1


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
    list_display = (
        'batch_id',
        'medicine',
        'batch_number',
        'quantity',
        'expiry_date',
        'is_expired'
    )
    search_fields = ('medicine__name', 'batch_number')
    list_filter = ('expiry_date',)

    def is_expired(self, obj):
        return obj.expiry_date < timezone.now().date()
    is_expired.boolean = True
    is_expired.short_description = "Expired"


# ------------------------------
# Medicine Stock Log Admin
# ------------------------------
@admin.register(MedicineStockLog)
class MedicineStockLogAdmin(admin.ModelAdmin):
    list_display = (
        'log_id',
        'batch',
        'change_type',
        'quantity_changed',
        'created_at'
    )
    search_fields = (
        'batch__batch_number',
        'batch__medicine__name'
    )
    list_filter = ('change_type', 'created_at')


# ------------------------------
# Dispense Admin
# ------------------------------
@admin.register(Dispense)
class DispenseAdmin(admin.ModelAdmin):

    inlines = [DispenseItemInline]

    list_display = (
        'dispense_id',
        'prescription',
        'get_patient',
        'total_amount',
        'status',
        'dispense_date'
    )

    search_fields = (
        'prescription__prescription_code',
        'patient__first_name',
        'patient__last_name'
    )

    list_filter = ('status', 'dispense_date')

    def get_patient(self, obj):
        return obj.patient
    get_patient.short_description = "Patient"


# ------------------------------
# Dispense Item Admin
# ------------------------------
@admin.register(DispenseItem)
class DispenseItemAdmin(admin.ModelAdmin):
    list_display = (
        'dispense',
        'batch',
        'get_medicine',
        'quantity',
        'price'
    )
    search_fields = (
        'batch__batch_number',
        'batch__medicine__name'
    )

    def get_medicine(self, obj):
        return obj.batch.medicine.name
    get_medicine.short_description = "Medicine"


# ------------------------------
# Medicine Bill Admin
# ------------------------------
@admin.register(MedicineBill)
class MedicineBillAdmin(admin.ModelAdmin):
    list_display = (
        'bill_id',
        'dispense',
        'get_patient',
        'total_amount',
        'discount',
        'final_amount',
        'payment_status',
        'created_at'
    )
    search_fields = (
        'dispense__dispense_id',
        'dispense__patient__first_name'
    )
    list_filter = ('payment_status', 'created_at')

    def get_patient(self, obj):
        return obj.dispense.patient
    get_patient.short_description = "Patient"