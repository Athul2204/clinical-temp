# from rest_framework import serializers
# from .models import (
#     Medicine, MedicineBatch, Dispense,
#     DispenseItem, MedicineBill, MedicineStockLog
# )


# class MedicineSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Medicine
#         fields = "__all__"


# class MedicineBatchSerializer(serializers.ModelSerializer):
#     medicine = MedicineSerializer(read_only=True)

#     class Meta:
#         model = MedicineBatch
#         fields = "__all__"


# class DispenseItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DispenseItem
#         fields = "__all__"


# class DispenseSerializer(serializers.ModelSerializer):
#     items = DispenseItemSerializer(many=True)

#     class Meta:
#         model = Dispense
#         fields = "__all__"

#     def create(self, validated_data):
#         items_data = validated_data.pop("items")
#         dispense = Dispense.objects.create(**validated_data)
#         for item in items_data:
#             DispenseItem.objects.create(
#                 dispense=dispense,
#                 **item
#             )
#         return dispense


# class MedicineBillSerializer(serializers.ModelSerializer):
#     dispense = DispenseSerializer(read_only=True)

#     class Meta:
#         model = MedicineBill
#         fields = "__all__"


# class MedicineStockLogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MedicineStockLog
#         fields = "__all__"



# from rest_framework import serializers
# from .models import Medicine, MedicineBatch, MedicineStockLog, Dispense, DispenseItem, MedicineBill

# # ------------------------------
# # Medicine Serializer
# # ------------------------------
# class MedicineSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Medicine
#         fields = '__all__'

# # ------------------------------
# # Medicine Batch Serializer
# # ------------------------------
# class MedicineBatchSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MedicineBatch
#         fields = '__all__'

# # ------------------------------
# # Medicine Stock Log Serializer
# # ------------------------------
# class MedicineStockLogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MedicineStockLog
#         fields = '__all__'

# # ------------------------------
# # Dispense Item Serializer
# # ------------------------------
# class DispenseItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DispenseItem
#         fields = '__all__'

# # ------------------------------
# # Dispense Serializer
# # ------------------------------
# class DispenseSerializer(serializers.ModelSerializer):
#     items = DispenseItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = Dispense
#         fields = '__all__'

# # ------------------------------
# # Medicine Bill Serializer
# # ------------------------------
# class MedicineBillSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MedicineBill
#         fields = '__all__'
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from .models import (
    Medicine, MedicineBatch, MedicineStockLog,
    Dispense, DispenseItem, MedicineBill
)


# ------------------------------
# Medicine Serializer
# ------------------------------
class MedicineSerializer(serializers.ModelSerializer):
    #serializers.SerializerMethodField(),This tells DRF:,This field value will be calculated by a function
    total_stock = serializers.SerializerMethodField()
    expired_stock = serializers.SerializerMethodField()
    expiring_soon_stock = serializers.SerializerMethodField()

 
    class Meta:
        model = Medicine
        fields = '__all__'
    #Important rule in DRF:SerializerMethodField uses get_<fieldname>,Since field name is:,total_stock,function must be:,get_total_stock
    def get_total_stock(self, obj):
        #medicine = models.ForeignKey(Medicine),Django automatically creates:,medicinebatch_set,Meaning:,all batches belonging to this medicine,,.all(),.So:,,batches = all batches of that medicine
        batches = obj.medicinebatch_set.all()
        total = sum(batch.quantity for batch in batches)
        return total
    def get_expired_stock(self, obj):
        today = timezone.now().date()
        batches = obj.medicinebatch_set.filter(expiry_date__lt=today)
        return sum(batch.quantity for batch in batches)

    def get_expiring_soon_stock(self, obj):
        today = timezone.now().date()
        next_30 = today + timedelta(days=30)

        batches = obj.medicinebatch_set.filter(
            expiry_date__gte=today,
            expiry_date__lte=next_30
        )

    #Field-level validation
    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Medicine name cannot be blank or whitespace.")
        return value.strip()  # clean up extra spaces

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Medicine price must be greater than zero.")
        return value


# ------------------------------
# Medicine Batch Serializer
# ------------------------------
class MedicineBatchSerializer(serializers.ModelSerializer):
    medicine= serializers.PrimaryKeyRelatedField(    # ← for POST/PATCH (send just the ID)
        queryset=Medicine.objects.all(),
        
        write_only=True
    )
    medicine_details = MedicineSerializer(source='medicine',read_only=True) 
    class Meta:
        model = MedicineBatch
        fields = '__all__'

    # ✅ Field-level validation
    def validate_expiry_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Expiry date must be a future date.")
        return value

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Batch quantity must be at least 1.")
        return value

    # ✅ Object-level validation (cross-field)
    def validate(self, data):
        medicine = data.get('medicine')
        batch_number = data.get('batch_number')

        # On update, exclude current instance from uniqueness check
        instance = self.instance
        qs = MedicineBatch.objects.filter(medicine=medicine, batch_number=batch_number)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "A batch with this batch number already exists for this medicine."
            )
        return data
    def create(self, validated_data):
        with transaction.atomic():

            batch = super().create(validated_data)

            MedicineStockLog.objects.create(
                batch=batch,
                change_type='ADD',
                quantity_changed=batch.quantity,
                remarks="Batch added to inventory"
            )

        return batch
    
# ------------------------------
# Medicine Stock Log Serializer
# ------------------------------
class MedicineStockLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineStockLog
        fields = '__all__'

    def validate_quantity_changed(self, value):
        if value == 0:
            raise serializers.ValidationError("Quantity changed cannot be zero.")
        return value

    # ✅ Object-level: direction vs change_type
    def validate(self, data):
        change_type = data.get('change_type')
        quantity_changed = data.get('quantity_changed')
        batch = data.get('batch')

        if change_type in ('DISPENSE', 'EXPIRED') and quantity_changed and quantity_changed > 0:
            raise serializers.ValidationError({
                'quantity_changed': f'{change_type} must be a negative value (stock going out).'
            })

        if change_type == 'ADD' and quantity_changed and quantity_changed < 0:
            raise serializers.ValidationError({
                'quantity_changed': 'ADD must be a positive value (stock coming in).'
            })

        # ✅ Cannot dispense more than available stock
        if change_type == 'DISPENSE' and batch and quantity_changed:
            if abs(quantity_changed) > batch.quantity:
                raise serializers.ValidationError({
                    'quantity_changed': (
                        f'Cannot dispense {abs(quantity_changed)} units. '
                        f'Only {batch.quantity} available in batch.'
                    )
                })

        return data

# pharmacy/serializers.py

from rest_framework import serializers
from reception.models import Patient


class PatientMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ["patient_id", "first_name", "last_name"]

#This is only for response display.
# ------------------------------
# Dispense Item Serializer
# ------------------------------
class DispenseItemSerializer(serializers.ModelSerializer):
    price=serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    class Meta:
        model = DispenseItem
        fields = '__all__'
        read_only_fields = ['price', 'dispense'] 
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value

   

    # ✅ Object-level: stock and expiry checks
    def validate(self, data):
        batch = data.get('batch')
        quantity = data.get('quantity')
        price = data.get('price')

        if batch:
            # Check expiry
            if batch.expiry_date < timezone.now().date():
                raise serializers.ValidationError({
                    'batch': f'Batch {batch.batch_number} has expired. Cannot dispense.'
                })

            # Check stock availability
            if quantity and quantity > batch.quantity:
                raise serializers.ValidationError({
                    'quantity': (
                        f'Requested quantity {quantity} exceeds '
                        f'available stock of {batch.quantity}.'
                    )
                })

            # Price must match medicine price
            

        return data
    #dispense serializer
# ------------------------------
class DispenseSerializer(serializers.ModelSerializer):
    total_amount=serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    items = DispenseItemSerializer(many=True)  # nested items
    patient = serializers.SerializerMethodField()
    class Meta:
        model = Dispense
        fields = ['dispense_id','prescription','patient','items','status','dispense_date','total_amount']
    def get_patient(self, obj):

        patient = obj.prescription.consultation.appointment.patient
        return PatientMiniSerializer(patient).data
    def validate_total_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Total amount must be greater than zero.")
        return value

    # ✅ Object-level: prevent duplicate dispense for same prescription
    def validate(self, data):
        prescription = data.get('prescription')
        instance = self.instance

        if prescription:
            qs = Dispense.objects.filter(prescription=prescription, status='Completed')
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError({
                    'prescription': 'This prescription has already been dispensed.'
                })

        return data
    def create(self, validated_data):

        items_data = validated_data.pop('items')

        prescription = validated_data.get('prescription')
        with transaction.atomic():
            patient = prescription.consultation.appointment.patient
            validated_data['patient'] = patient
            validated_data['total_amount'] = 0
            dispense = Dispense.objects.create(**validated_data)

            total_amount = 0

            for item in items_data:

                batch = item['batch']
                quantity = item['quantity']
                if quantity > batch.quantity:
                    raise serializers.ValidationError(
                        f"Not enough stock in batch {batch.batch_number}. Only {batch.quantity} available."
                    )

                price = batch.medicine.price
                item_total = price * quantity

                DispenseItem.objects.create(
                    dispense=dispense,
                    batch=batch,
                    quantity=quantity,
                    price=price
                )

            # reduce stock
                batch.quantity -= quantity
                batch.save()

                # create stock log
                MedicineStockLog.objects.create(
                    batch=batch,
                    change_type='DISPENSE',
                    quantity_changed=-quantity
                )

                total_amount += item_total

            dispense.total_amount = total_amount
            dispense.status = "Completed"
            dispense.save()

            return dispense


# ------------------------------
# Medicine Bill Serializer
# ------------------------------
class MedicineBillSerializer(serializers.ModelSerializer):
    final_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = MedicineBill
        fields = '__all__'
        read_only_fields = ['final_amount', 'created_at']

    def validate_total_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Total amount must be greater than zero.")
        return value

    def validate_discount(self, value):
        if value < 0:
            raise serializers.ValidationError("Discount cannot be negative.")
        return value

    # ✅ Object-level: discount < total, bill matches dispense total
    def validate(self, data):
        total_amount = data.get('total_amount')
        discount = data.get('discount', 0)
        dispense = data.get('dispense')

        # Discount must not exceed total
        if total_amount and discount and discount > total_amount:
            raise serializers.ValidationError({
                'discount': 'Discount cannot exceed the total amount.'
            })

        # Bill total must match dispense total
        if dispense and total_amount and total_amount != dispense.total_amount:
            raise serializers.ValidationError({
                'total_amount': (
                    f'Bill total ({total_amount}) must match '
                    f'the dispense total ({dispense.total_amount}).'
                )
            })

        # ✅ Prevent duplicate bill for same dispense (on create)
        instance = self.instance
        if dispense:
            qs = MedicineBill.objects.filter(dispense=dispense)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError({
                    'dispense': 'A bill already exists for this dispense.'
                })

        return data