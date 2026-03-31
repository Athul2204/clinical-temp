
# from rest_framework import serializers
# from django.utils import timezone
# from datetime import timedelta
# from django.db import transaction
# from rest_framework.exceptions import ValidationError
# from doctor.models import PrescriptionItem

# from doctor.models import Prescription, PrescriptionItem
# import re
# from .models import (
#     Medicine, MedicineBatch, MedicineStockLog,
#     Dispense, DispenseItem, MedicineBill
# )


# # ------------------------------
# # Medicine Serializer
# # ------------------------------
# class MedicineSerializer(serializers.ModelSerializer):
#     #serializers.SerializerMethodField(),This tells DRF:,This field value will be calculated by a function
#     total_stock = serializers.SerializerMethodField()
#     expired_stock = serializers.SerializerMethodField()
#     expiring_soon_stock = serializers.SerializerMethodField()

 
#     class Meta:
#         model = Medicine
#         fields = '__all__'
#     #Important rule in DRF:SerializerMethodField uses get_<fieldname>,Since field name is:,total_stock,function must be:,get_total_stock
#     # def get_total_stock(self, obj):
#     #     #medicine = models.ForeignKey(Medicine),Django automatically creates:,medicinebatch_set,Meaning:,all batches belonging to this medicine,,.all(),.So:,,batches = all batches of that medicine
#     #     batches = obj.batches.all()
#     #     total = sum(batch.quantity for batch in batches)
#     #     return total
#     def get_total_stock(self, obj):
#         today = timezone.now().date()
#         batches = obj.batches.filter(expiry_date__gte=today)
#         total = sum(batch.quantity for batch in batches)
#         return total
#     def get_expired_stock(self, obj):
#         today = timezone.now().date()
#         batches = obj.batches.filter(expiry_date__lt=today)
#         return sum(batch.quantity for batch in batches)

#     def get_expiring_soon_stock(self, obj):
#         today = timezone.now().date()
#         next_30 = today + timedelta(days=30)

#         batches = obj.batches.filter(
#             expiry_date__gte=today,
#             expiry_date__lte=next_30
#         )
#         return sum(batch.quantity for batch in batches)
#     #Field-level validation
#     def validate_name(self, value):
#         if not value.strip():
#             raise serializers.ValidationError("Medicine name cannot be blank or whitespace.")
#         return value.strip()  # clean up extra spaces

#     def validate_price(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Medicine price must be greater than zero.")
#         return value


# # ------------------------------
# # Medicine Batch Serializer
# # ------------------------------
# class MedicineBatchSerializer(serializers.ModelSerializer):
#     medicine= serializers.PrimaryKeyRelatedField(    # ← for POST/PATCH (send just the ID)
#         queryset=Medicine.objects.all(),
        
#         write_only=True
#     )
#     medicine_details = MedicineSerializer(source='medicine',read_only=True) 
#     batch_number = serializers.CharField(required=False, allow_blank=True)

#     class Meta:
#         model = MedicineBatch
#         fields = '__all__'

#     # Field-level validation
#     def validate_expiry_date(self, value):
#         if value < timezone.now().date():
#             raise serializers.ValidationError("Expiry date must be a future date.")
#         return value

#     def validate_quantity(self, value):
#         if value < 1:
#             raise serializers.ValidationError("Batch quantity must be at least 1.")
#         return value
#     # def validate_batch_number(self, value):
#     #     if value:  # only validate if user sends it
#     #         if not re.match(r'^B\d{3}$', value):
#     #             raise serializers.ValidationError(
#     #                 "Batch number must be in format B001, B002, etc."
#     #             )
#     #     return value
#     # def validate_batch_number(self, value):
#     #     if value:  
#     #         if MedicineBatch.objects.filter(batch_number=value).exists():
#     #             raise serializers.ValidationError("Batch number already exists.")
#     #         return value
#     def validate_batch_number(self, value):
#         if value:
#             if not re.match(r'^B\d{3}$', value):
#                 raise serializers.ValidationError("Batch number must be in format B001, B002.")
#             if MedicineBatch.objects.filter(batch_number=value).exists():
#                 raise serializers.ValidationError("Batch number already exists.")
#         return value
        
    
# # ------------------------------
# # Medicine Stock Log Serializer
# # ------------------------------
# class MedicineStockLogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MedicineStockLog
#         fields = '__all__'

#     def validate_quantity_changed(self, value):
#         if value == 0:
#             raise serializers.ValidationError("Quantity changed cannot be zero.")
#         return value

#     # Object-level: direction vs change_type
#     def validate(self, data):
#         change_type = data.get('change_type')
#         quantity_changed = data.get('quantity_changed')
#         batch = data.get('batch')

#         if change_type in ('DISPENSE', 'EXPIRED') and quantity_changed and quantity_changed > 0:
#             raise serializers.ValidationError({
#                 'quantity_changed': f'{change_type} must be a negative value (stock going out).'
#             })

#         if change_type == 'ADD' and quantity_changed and quantity_changed < 0:
#             raise serializers.ValidationError({
#                 'quantity_changed': 'ADD must be a positive value (stock coming in).'
#             })

#         #  Cannot dispense more than available stock
#         if change_type == 'DISPENSE' and batch and quantity_changed:
#             if abs(quantity_changed) > batch.quantity:
#                 raise serializers.ValidationError({
#                     'quantity_changed': (
#                         f'Cannot dispense {abs(quantity_changed)} units. '
#                         f'Only {batch.quantity} available in batch.'
#                     )
#                 })

#         return data

# # pharmacy/serializers.py

# from rest_framework import serializers
# from reception.models import Patient


# class PatientMiniSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Patient
#         fields = ["patient_id", "first_name", "last_name"]

# #This is only for response display.
# # ------------------------------
# # Dispense Item Serializer
# # ------------------------------
# class DispenseItemSerializer(serializers.ModelSerializer):
#     price=serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
#     class Meta:
#         model = DispenseItem
#         fields = '__all__'
#         read_only_fields = ['price', 'dispense'] 
#     def validate_quantity(self, value):
#         if value < 1:
#             raise serializers.ValidationError("Quantity must be at least 1.")
#         return value

   

#     #  Object-level: stock and expiry checks
#     def validate(self, data):
#         batch = data.get('batch')
#         quantity = data.get('quantity')
#         price = data.get('price')

#         if batch:
#             # Check expiry
#             if batch.expiry_date < timezone.now().date():
#                 raise serializers.ValidationError({
#                     'batch': f'Batch {batch.batch_number} has expired. Cannot dispense.'
#                 })

            
            

#         return data
#     #dispense serializer
# # ------------------------------
# class DispenseSerializer(serializers.ModelSerializer):
#     total_amount=serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
#     items = DispenseItemSerializer(many=True)  # nested items
#     patient = serializers.SerializerMethodField()
#     class Meta:
#         model = Dispense
#         fields = ['dispense_id','prescription','patient','items','status','dispense_date','total_amount']
#     def get_patient(self, obj):

#         patient = obj.prescription.consultation.appointment.patient
#         return PatientMiniSerializer(patient).data
#     def validate_total_amount(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Total amount must be greater than zero.")
#         return value

#     # ✅ Object-level: prevent duplicate dispense for same prescription
#     def validate(self, data):
#         prescription = data.get('prescription')
#         instance = self.instance

#         if prescription:
#             qs = Dispense.objects.filter(prescription=prescription, status='Completed')
#             if instance:
#                 qs = qs.exclude(pk=instance.pk)
#             if qs.exists():
#                 raise serializers.ValidationError({
#                     'prescription': 'This prescription has already been dispensed.'
#                 })

#         return data
#     def create(self, validated_data):

#         items_data = validated_data.pop('items')

#         prescription = validated_data.get('prescription')
#             #  1. Prescription must be SENT
#         if prescription.status != "Sent":
#             raise ValidationError("Prescription must be sent before dispensing.")

#         #  2. Get allowed medicines from prescription
#         prescription_items = PrescriptionItem.objects.filter(prescription=prescription)

#         allowed_medicines = [
#             item.medicine_name for item in prescription_items
#         ]

#         # 3. Prevent duplicate medicine entries (optional but good)
#         seen_medicines = set()
#         for item in items_data:
#             medicine = item['batch'].medicine
#             if medicine in seen_medicines:
#                 raise ValidationError(f"{medicine.name} added multiple times.")
#             seen_medicines.add(medicine)
#         with transaction.atomic():
#             patient = prescription.consultation.appointment.patient
#             validated_data['patient'] = patient
#             validated_data['total_amount'] = 0
#             dispense = Dispense.objects.create(**validated_data)

#             total_amount = 0
#             for item in items_data:
#                 batch = item['batch']
#                 requested_qty = item['quantity']
#                 medicine = batch.medicine
#                 medicine_name = medicine.name
#                 # ✅ 4. Medicine must be in prescription
#                 if medicine not in allowed_medicines:
#                     raise ValidationError(
#                         f"{medicine_name} is not in the doctor's prescription."
#                     )
#                 #  CASE 1: NO STOCK
#                 if batch.quantity == 0:
#                     DispenseItem.objects.create(
#                         dispense=dispense,
#                         batch=batch,
#                         quantity=0,
#                         price=batch.medicine.price,
#                         remarks=f"{medicine_name} is not available. Please purchase from outside."
#                     )
#                     continue

#                 #  CASE 2: PARTIAL STOCK
#                 if requested_qty > batch.quantity:
#                     dispensed_qty = batch.quantity

#                     DispenseItem.objects.create(
#                         dispense=dispense,
#                         batch=batch,
#                         quantity=dispensed_qty,
#                         price=batch.medicine.price,
#                         remarks=(
#                             f"{medicine_name}: Only {dispensed_qty} available. "
#                             f"Remaining to be purchased outside."
#                         )
#                     )

#                     total_amount += batch.medicine.price * dispensed_qty
                    
#                     continue

#                 #  CASE 3: FULL STOCK
#                 DispenseItem.objects.create(
#                     dispense=dispense,
#                     batch=batch,
#                     quantity=requested_qty,
#                     price=batch.medicine.price,
#                     remarks=None
#                 )

#                 total_amount += batch.medicine.price * requested_qty
                

#             dispense.total_amount = total_amount
#             dispense.status = "Completed"
#             dispense.save()
#             prescription = dispense.prescription
#             prescription.status = "Dispensed"
#             prescription.dispensed_at = timezone.now()
#             prescription.save(update_fields=["status", "dispensed_at"])

#             return dispense


# # ------------------------------
# # Medicine Bill Serializer
# # ------------------------------
# class MedicineBillSerializer(serializers.ModelSerializer):
#     final_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
#     items=DispenseItemSerializer(source='dispense.items',many=True,read_only=True)
#     patient = serializers.SerializerMethodField()
#     class Meta:
#         model = MedicineBill
#         fields = '__all__'
#         read_only_fields = ['final_amount', 'created_at']
#     def get_patient(self, obj):

#         patient = obj.dispense.prescription.consultation.appointment.patient
#         return PatientMiniSerializer(patient).data

#     def validate_total_amount(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Total amount must be greater than zero.")
#         return value

#     def validate_discount(self, value):
#         if value < 0:
#             raise serializers.ValidationError("Discount cannot be negative.")
#         return value

#     # ✅ Object-level: discount < total, bill matches dispense total
#     def validate(self, data):
#         total_amount = data.get('total_amount')
#         discount = data.get('discount', 0)
#         dispense = data.get('dispense')

#         # Discount must not exceed total
#         if total_amount and discount and discount > total_amount:
#             raise serializers.ValidationError({
#                 'discount': 'Discount cannot exceed the total amount.'
#             })

#         # Bill total must match dispense total
#         if dispense and total_amount and total_amount != dispense.total_amount:
#             raise serializers.ValidationError({
#                 'total_amount': (
#                     f'Bill total ({total_amount}) must match '
#                     f'the dispense total ({dispense.total_amount}).'
#                 )
#             })

#         # ✅ Prevent duplicate bill for same dispense (on create)
#         instance = self.instance
#         if dispense:
#             qs = MedicineBill.objects.filter(dispense=dispense)
#             if instance:
#                 qs = qs.exclude(pk=instance.pk)
#             if qs.exists():
#                 raise serializers.ValidationError({
#                     'dispense': 'A bill already exists for this dispense.'
#                 })

#         return data


# class PrescriptionItemReadSerializer(serializers.ModelSerializer):
#     medicine_name = serializers.CharField(source='medicine_name.name')
#     medicine_id = serializers.IntegerField(source='medicine_name.medicine_id')

#     class Meta:
#         model = PrescriptionItem
#         fields = ['medicine_id', 'medicine_name', 'dosage', 'frequency', 'duration', 'instructions']

# class IncomingPrescriptionSerializer(serializers.ModelSerializer):
#     items = PrescriptionItemReadSerializer(many=True, read_only=True)
#     patient_name = serializers.SerializerMethodField()
#     doctor_name = serializers.SerializerMethodField()

#     class Meta:
#         model = Prescription
#         fields = ['id','prescription_code', 'status', 'created_at', 'sent_at', 'patient_name', 'doctor_name', 'items']

#     def get_patient_name(self, obj):
#         patient = obj.consultation.appointment.patient
#         return f"{patient.first_name} {patient.last_name}"

#     def get_doctor_name(self, obj):
#         return str(obj.doctor)
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from rest_framework.exceptions import ValidationError
from doctor.models import Prescription, PrescriptionItem
from reception.models import Patient

from .models import (
    Medicine, MedicineBatch, MedicineStockLog,
    Dispense, DispenseItem, MedicineBill
)


# ==============================
# PATIENT MINI SERIALIZER
# ==============================
class PatientMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["patient_id", "first_name", "last_name"]


# ==============================
# MEDICINE SERIALIZER
# ==============================
class MedicineSerializer(serializers.ModelSerializer):
    total_stock = serializers.SerializerMethodField()
    expired_stock = serializers.SerializerMethodField()
    expiring_soon_stock = serializers.SerializerMethodField()

    class Meta:
        model = Medicine
        fields = '__all__'

    def get_total_stock(self, obj):
        today = timezone.now().date()
        batches = obj.batches.filter(expiry_date__gte=today)
        return sum(batch.quantity for batch in batches)

    def get_expired_stock(self, obj):
        today = timezone.now().date()
        batches = obj.batches.filter(expiry_date__lt=today)
        return sum(batch.quantity for batch in batches)

    def get_expiring_soon_stock(self, obj):
        today = timezone.now().date()
        next_30 = today + timedelta(days=30)
        batches = obj.batches.filter(
            expiry_date__gte=today,
            expiry_date__lte=next_30
        )
        return sum(batch.quantity for batch in batches)

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Medicine name cannot be blank.")
        return value.strip()

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


# ==============================
# MEDICINE BATCH SERIALIZER
# ==============================
class MedicineBatchSerializer(serializers.ModelSerializer):
    medicine = serializers.PrimaryKeyRelatedField(
        queryset=Medicine.objects.all(),
        write_only=True
    )
    medicine_details = MedicineSerializer(source='medicine', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    medicine_price = serializers.DecimalField(
        source='medicine.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = MedicineBatch
        fields = '__all__'
        read_only_fields = ['batch_number', 'created_at']

    def validate_expiry_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Expiry must be future date.")
        return value

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Minimum quantity is 1.")
        return value


# ==============================
# STOCK LOG SERIALIZER
# ==============================
class MedicineStockLogSerializer(serializers.ModelSerializer):
    batch_details = serializers.SerializerMethodField()

    class Meta:
        model = MedicineStockLog
        fields = '__all__'
        read_only_fields = ['created_at']

    def get_batch_details(self, obj):
        return {
            'batch_number': obj.batch.batch_number,
            'medicine_name': obj.batch.medicine.name
        }

    def validate(self, data):
        change_type = data.get('change_type')
        qty = data.get('quantity_changed')

        if qty == 0:
            raise ValidationError("Quantity cannot be zero")

        if change_type == 'ADD' and qty < 0:
            raise ValidationError("ADD must be positive")

        if change_type in ['DISPENSE', 'EXPIRED'] and qty > 0:
            raise ValidationError("Must be negative for stock out")

        return data


# ==============================
# DISPENSE ITEM SERIALIZER
# ==============================
class DispenseItemSerializer(serializers.ModelSerializer):
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)
    medicine_name = serializers.CharField(source='batch.medicine.name', read_only=True)

    class Meta:
        model = DispenseItem
        fields = ['batch', 'batch_number', 'medicine_name', 'quantity', 'price']
        read_only_fields = ['price']

    def validate(self, data):
        batch = data.get('batch')
        qty = data.get('quantity')

        if not batch:
            raise ValidationError("Batch is required")

        if not qty:
            raise ValidationError("Quantity is required")

        if batch.expiry_date < timezone.now().date():
            raise ValidationError(f"Batch {batch.batch_number} expired")

        if qty > batch.quantity:
            raise ValidationError(
                f"Only {batch.quantity} units available in batch {batch.batch_number}"
            )

        return data


# ==============================
# DISPENSE SERIALIZER
# ==============================
class DispenseSerializer(serializers.ModelSerializer):
    items = DispenseItemSerializer(many=True)
    patient_details = serializers.SerializerMethodField(read_only=True)
    prescription_code = serializers.CharField(
        source='prescription.prescription_code', read_only=True
    )

    class Meta:
        model = Dispense
        fields = [
            'dispense_id',
            'prescription',
            'patient',
            'patient_details',
            'prescription_code',
            'items',
            'status',
            'dispense_date',
            'total_amount'
        ]
        read_only_fields = ['dispense_id', 'patient', 'dispense_date', 'total_amount']

    def get_patient_details(self, obj):
        patient = obj.patient
        return {
            'patient_id': patient.patient_id,
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'full_name': f"{patient.first_name} {patient.last_name}"
        }

    def validate(self, data):
        prescription = data.get('prescription')

        if not prescription:
            raise ValidationError("Prescription is required")

        if prescription.status != "Sent":
            raise ValidationError("Prescription must be in 'Sent' status")

        if Dispense.objects.filter(prescription=prescription, status='Completed').exists():
            raise ValidationError("Prescription already dispensed")

        items_data = data.get('items', [])
        if not items_data:
            raise ValidationError("At least one medicine item is required")

        return data

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        prescription = validated_data['prescription']

        patient = prescription.consultation.appointment.patient
        validated_data['patient'] = patient

        prescription_items = PrescriptionItem.objects.filter(prescription=prescription)
        allowed_medicine_ids = [item.medicine_name_id for item in prescription_items]

        total = 0
        validated_items = []

        for item_data in items_data:
            batch = item_data['batch']
            qty = item_data['quantity']
            medicine = batch.medicine

            if medicine.medicine_id not in allowed_medicine_ids:
                raise ValidationError(f"{medicine.name} is not in the prescription")

            item_total = qty * medicine.price
            total += item_total

            validated_items.append({
                'batch': batch,
                'quantity': qty,
                'price': medicine.price
            })

        validated_data['total_amount'] = total
        validated_data['status'] = 'Completed'
        dispense = Dispense.objects.create(**validated_data)

        for item_data in validated_items:
            DispenseItem.objects.create(
                dispense=dispense,
                batch=item_data['batch'],
                quantity=item_data['quantity']
            )

        prescription.status = "Dispensed"
        prescription.dispensed_at = timezone.now()
        prescription.save(update_fields=['status', 'dispensed_at'])

        return dispense


# ==============================
# MEDICINE BILL SERIALIZER
# ==============================
class MedicineBillSerializer(serializers.ModelSerializer):
    patient_details = serializers.SerializerMethodField(read_only=True)
    items = DispenseItemSerializer(source='dispense.items', many=True, read_only=True)
    prescription_code = serializers.CharField(
        source='dispense.prescription.prescription_code', read_only=True
    )

    class Meta:
        model = MedicineBill
        fields = [
            'bill_id',
            
            'dispense',
            'total_amount',
            'discount',
            'final_amount',
            'payment_status',
            'created_at',
            'patient_details',
            'prescription_code',
            'items'
        ]
        read_only_fields = ['bill_id', 'final_amount', 'created_at']

    def get_patient_details(self, obj):
        patient = obj.dispense.patient
        return {
            'patient_id': patient.patient_id,
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'full_name': f"{patient.first_name} {patient.last_name}"
        }

    def validate(self, data):
        # ✅ FIX: On PATCH (partial update), 'dispense' is not sent in the payload.
        # The old code did `data.get('dispense')` which returned None for PATCH,
        # then immediately raised "Dispense is required" — blocking Mark Paid entirely.
        # Fix: only run the create-time validations when dispense IS present in data
        # (i.e. during POST/create). For PATCH we only validate the fields being changed.

        dispense = data.get('dispense')
        total = data.get('total_amount')
        discount = data.get('discount', 0)

        # ── CREATE-ONLY validations (dispense must be present on create) ──
        if dispense is not None:
            if total is not None and total <= 0:
                raise ValidationError("Total must be greater than 0")

            if discount < 0:
                raise ValidationError("Discount cannot be negative")

            if total is not None and discount > total:
                raise ValidationError("Discount exceeds total amount")

            if total is not None and dispense.total_amount != total:
                raise ValidationError(
                    f"Bill total ({total}) must match dispense total ({dispense.total_amount})"
                )

            # Prevent duplicate bill for this dispense (on create only)
            instance = self.instance
            qs = MedicineBill.objects.filter(dispense=dispense)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise ValidationError("Bill already exists for this dispense")

        # ── PATCH-ONLY validations (payment_status update) ──
        payment_status = data.get('payment_status')
        if payment_status and payment_status not in ('Pending', 'Paid'):
            raise ValidationError("payment_status must be 'Pending' or 'Paid'")

        return data

    def create(self, validated_data):
        validated_data['final_amount'] = (
            validated_data['total_amount'] - validated_data.get('discount', 0)
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # ✅ On partial update (PATCH for Mark Paid), only update the fields sent.
        # Recalculate final_amount if total_amount or discount changed.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if 'total_amount' in validated_data or 'discount' in validated_data:
            instance.final_amount = instance.total_amount - (instance.discount or 0)

        instance.save()
        return instance


# ==============================
# PRESCRIPTION ITEM READ SERIALIZER
# ==============================
class PrescriptionItemReadSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine_name.name')
    medicine_id = serializers.IntegerField(source='medicine_name.medicine_id')
    medicine_price = serializers.DecimalField(
        source='medicine_name.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = PrescriptionItem
        fields = [
            'medicine_id',
            'medicine_name',
            'medicine_price',
            'dosage',
            'frequency',
            'duration',
            'instructions'
        ]


# ==============================
# INCOMING PRESCRIPTION SERIALIZER
# ==============================
class IncomingPrescriptionSerializer(serializers.ModelSerializer):
    items = PrescriptionItemReadSerializer(many=True, read_only=True)
    patient_name = serializers.SerializerMethodField()
    patient_id = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    diagnosis = serializers.CharField(source='consultation.diagnosis', read_only=True)
    prescription_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Prescription
        fields = [
            'id',
            'prescription_id',
            'prescription_code',
            'status',
            'created_at',
            'sent_at',
            'patient_id',
            'patient_name',
            'doctor_name',
            'diagnosis',
            'items'
        ]

    def get_patient_id(self, obj):
        return obj.consultation.appointment.patient.patient_id

    def get_patient_name(self, obj):
        p = obj.consultation.appointment.patient
        return f"{p.first_name} {p.last_name}"

    def get_doctor_name(self, obj):
        return str(obj.doctor)