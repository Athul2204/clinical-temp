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

def get_prescribed_qty(p_item):
    try:
        freq = int(p_item.frequency)
    except (TypeError, ValueError):
        freq = 1
    duration = p_item.duration or 1
    return freq * duration
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
# ✅ BILLING GATE: Medicine can only be dispensed AFTER the MedicineBill for
#    this prescription's dispense record has been created AND marked Paid.
#    Flow:  Prescription received → Dispense created (Pending) →
#           MedicineBill generated → Bill paid → Dispense completed / medicines handed over.
#
#    NOTE: The Dispense is created first (status=Pending) so that the bill can
#    reference it. Actual stock deduction happens when the bill is paid and the
#    pharmacist finalises the dispense.
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

        # ✅ BILLING GATE: Check the consultation bill (reception) is paid first.
        #    Pharmacist should not handle any prescription until the patient has
        #    settled the doctor's consultation fee at the reception counter.
        try:
            consultation_bill = prescription.consultation.appointment.bill
            if consultation_bill.status != "Paid":
                raise ValidationError(
                    "Cannot process this prescription. "
                    "The patient's consultation bill at reception is not yet paid. "
                    f"Bill status: {consultation_bill.status}."
                )
        except Exception as e:
            if "Cannot process" in str(e):
                raise
            raise ValidationError(f"Cannot verify consultation billing status: {str(e)}")

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
# ✅ The MedicineBill is the pharmacy's own bill (separate from the lab bill and
#    the consultation bill).  It is created when the pharmacist confirms the
#    medicines to dispense. Only after this bill is marked Paid is the Dispense
#    finalised and medicines handed to the patient (enforced in DispenseSerializer).
class MedicineBillSerializer(serializers.ModelSerializer):
    patient_details = serializers.SerializerMethodField(read_only=True)
    #items = DispenseItemSerializer(source='dispense.items', many=True, read_only=True)
    doctor_name = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    bill_note = serializers.SerializerMethodField()
    dispense_date = serializers.DateTimeField(source='dispense.dispense_date', read_only=True)
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
            # 'items'
            'doctor_name',
            'dispense_date',
            'items',
            'bill_note'
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
    def get_items(self, obj):
        dispense = obj.dispense
        prescription = dispense.prescription

        prescription_items = prescription.items.select_related("medicine_name")
        dispense_items = dispense.items.select_related("batch__medicine")

        result = []

        for p_item in prescription_items:
            medicine = p_item.medicine_name

            # calculate prescribed quantity
            try:
                freq = int(p_item.frequency)
            except:
                freq = 1
            duration = p_item.duration or 1
            prescribed_qty = freq * duration

            # get dispensed items for this medicine
            matching_dispense = [
                d for d in dispense_items
                if d.batch.medicine_id == medicine.medicine_id
            ]

            dispensed_qty = sum(d.quantity for d in matching_dispense)
            remaining_qty = max(prescribed_qty - dispensed_qty, 0)

            line_total = sum(d.quantity * d.price for d in matching_dispense)
            batch_numbers = [d.batch.batch_number for d in matching_dispense]

            is_partial = remaining_qty > 0

            note = ""
            if is_partial:
                note = (
                    f"Only {dispensed_qty} unit(s) were available. "
                    f"Please purchase remaining {remaining_qty} unit(s) from another pharmacy."
                )

            result.append({
                "medicine_name": medicine.name,
                "batch_numbers": batch_numbers,
                "dosage": p_item.dosage,
                "instructions": p_item.instructions or "",
                "prescribed_quantity": prescribed_qty,
                "dispensed_quantity": dispensed_qty,
                "remaining_quantity": remaining_qty,
                "unit_price": medicine.price,
                "line_total": line_total,
                "is_partial": is_partial,
                "note": note
            })

        return result
    def get_doctor_name(self, obj):
        doctor = obj.dispense.prescription.doctor
        return str(doctor)
    def get_bill_note(self, obj):
        items = self.get_items(obj)

        if any(item["is_partial"] for item in items):
            return "Some medicines were not fully available in our pharmacy."

        return ""
    def validate(self, data):
        dispense = data.get('dispense')
        total = data.get('total_amount')
        discount = data.get('discount', 0)

        # CREATE-time validations (dispense present in payload)
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

            instance = self.instance
            qs = MedicineBill.objects.filter(dispense=dispense)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise ValidationError("Bill already exists for this dispense")

        # PATCH-time validations
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
# ✅ FIX: Added appointment_id field so the frontend billing gate can call
#    GET /api/reception/appointments-by-date/?appointment_id=<id>
#    to verify the consultation bill status before showing dispense options.
class IncomingPrescriptionSerializer(serializers.ModelSerializer):
    items = PrescriptionItemReadSerializer(many=True, read_only=True)
    patient_name = serializers.SerializerMethodField()
    patient_id = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    diagnosis = serializers.CharField(source='consultation.diagnosis', read_only=True)
    prescription_id = serializers.IntegerField(source='id', read_only=True)
    appointment_id = serializers.SerializerMethodField()   # ✅ NEW

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
            'appointment_id',    # ✅ NEW
            'items'
        ]

    def get_patient_id(self, obj):
        return obj.consultation.appointment.patient.patient_id

    def get_patient_name(self, obj):
        p = obj.consultation.appointment.patient
        return f"{p.first_name} {p.last_name}"

    def get_doctor_name(self, obj):
        return str(obj.doctor)

    def get_appointment_id(self, obj):
        return obj.consultation.appointment.appointment_id