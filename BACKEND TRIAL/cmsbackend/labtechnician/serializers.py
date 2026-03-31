# from rest_framework import serializers
# from .models import (
#     LabTest, LabOrder, LabOrderItem,
#     LabResult, LabBill, LabEquipment, LabMaintenance
# )


# class LabTestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabTest
#         fields = "__all__"


# class LabOrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabOrderItem
#         fields = "__all__"


# class LabOrderSerializer(serializers.ModelSerializer):
#     items = LabOrderItemSerializer(many=True)

#     class Meta:
#         model = LabOrder
#         fields = "__all__"

#     def create(self, validated_data):
#         items_data = validated_data.pop("items")
#         lab_order = LabOrder.objects.create(**validated_data)
#         for item in items_data:
#             LabOrderItem.objects.create(
#                 lab_order=lab_order,
#                 **item
#             )
#         return lab_order


# class LabResultSerializer(serializers.ModelSerializer):
#     lab_order = LabOrderSerializer(read_only=True)

#     class Meta:
#         model = LabResult
#         fields = "__all__"


# class LabBillSerializer(serializers.ModelSerializer):
#     lab_order = LabOrderSerializer(read_only=True)

#     class Meta:
#         model = LabBill
#         fields = "__all__"


# class LabEquipmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabEquipment
#         fields = "__all__"


# class LabMaintenanceSerializer(serializers.ModelSerializer):
#     equipment = LabEquipmentSerializer(read_only=True)

#     class Meta:
#         model = LabMaintenance
#         fields = "__all__"

# from rest_framework import serializers
# from .models import LabTest, LabOrder, LabOrderItem, LabResult, LabBill, LabEquipment, LabMaintenance

# # ------------------------------
# # Lab Test Serializer
# # ------------------------------
# class LabTestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabTest
#         fields = '__all__'

# # ------------------------------
# # Lab Order Item Serializer
# # ------------------------------
# class LabOrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabOrderItem
#         fields = '__all__'

# # ------------------------------
# # Lab Order Serializer
# # ------------------------------
# class LabOrderSerializer(serializers.ModelSerializer):
#     items = LabOrderItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = LabOrder
#         fields = '__all__'

# # ------------------------------
# # Lab Result Serializer
# # ------------------------------
# class LabResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabResult
#         fields = '__all__'

# # ------------------------------
# # Lab Bill Serializer
# # ------------------------------
# class LabBillSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabBill
#         fields = '__all__'

# # ------------------------------
# # Lab Equipment Serializer
# # ------------------------------
# class LabEquipmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabEquipment
#         fields = '__all__'

# # ------------------------------
# # Lab Maintenance Serializer
# # ------------------------------
# class LabMaintenanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabMaintenance
#         fields = '__all__'


# from rest_framework import serializers
# from .models import LabTest, LabOrder, LabOrderItem, LabResult, LabBill, LabEquipment, LabMaintenance

# # ------------------------------
# # Lab Test Serializer
# # ------------------------------
# class LabTestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabTest
#         fields = '__all__'

#     def validate_test_name(self, value):
#         cleaned = value.strip()
#         if not cleaned:
#             raise serializers.ValidationError("Test name cannot be empty.")

#         exists = LabTest.objects.filter(test_name__iexact=cleaned)
#         if self.instance:
#             exists = exists.exclude(pk=self.instance.pk)
#         if exists.exists():
#             raise serializers.ValidationError("A lab test with this name already exists.")
#         return cleaned

# # ------------------------------
# # Lab Order Item Serializer
# # ------------------------------
# class LabOrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabOrderItem
#         fields = '__all__'

#     def validate(self, attrs):
#         lab_order = attrs.get("lab_order") or getattr(self.instance, "lab_order", None)
#         lab_test = attrs.get("lab_test") or getattr(self.instance, "lab_test", None)

#         if lab_order and lab_order.status == "Completed":
#             raise serializers.ValidationError(
#                 {"lab_order": "Cannot modify items for a completed lab order."}
#             )

#         if lab_order and lab_test:
#             duplicate = LabOrderItem.objects.filter(
#                 lab_order=lab_order,
#                 lab_test=lab_test,
#             )
#             if self.instance:
#                 duplicate = duplicate.exclude(pk=self.instance.pk)
#             if duplicate.exists():
#                 raise serializers.ValidationError(
#                     {"lab_test": "This test is already part of the selected order."}
#                 )
#         return attrs

# # ------------------------------
# # Lab Order Serializer
# # ------------------------------
# class LabOrderSerializer(serializers.ModelSerializer):
#     items = LabOrderItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = LabOrder
#         fields = '__all__'

#     def validate(self, attrs):
#         lab_request = attrs.get("lab_request") or getattr(self.instance, "lab_request", None)
#         patient = attrs.get("patient") or getattr(self.instance, "patient", None)

#         if lab_request and patient:
#             expected_patient = lab_request.consultation.appointment.patient
#             if patient.pk != expected_patient.pk:
#                 raise serializers.ValidationError(
#                     {"patient": "Patient must match the patient from the linked lab request."}
#                 )
#         return attrs

# # ------------------------------
# # Lab Result Serializer
# # ------------------------------
# class LabResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabResult
#         fields = '__all__'

#     def validate_result_value(self, value):
#         cleaned = value.strip()
#         if not cleaned:
#             raise serializers.ValidationError("Result value cannot be empty.")
#         return cleaned

#     def _sync_order_status(self, lab_order):
#         has_items = lab_order.items.exists()
#         all_completed = has_items and not lab_order.items.filter(labresult__isnull=True).exists()
#         desired_status = "Completed" if all_completed else "Pending"
#         if lab_order.status != desired_status:
#             lab_order.status = desired_status
#             lab_order.save(update_fields=["status"])

#     def create(self, validated_data):
#         result = super().create(validated_data)
#         self._sync_order_status(result.lab_order_item.lab_order)
#         return result

#     def update(self, instance, validated_data):
#         result = super().update(instance, validated_data)
#         self._sync_order_status(result.lab_order_item.lab_order)
#         return result

# # ------------------------------
# # Lab Bill Serializer
# # ------------------------------
# class LabBillSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabBill
#         fields = '__all__'

#     def validate(self, attrs):
#         total_amount = attrs.get("total_amount", getattr(self.instance, "total_amount", 0))
#         discount = attrs.get("discount", getattr(self.instance, "discount", 0))
#         lab_order = attrs.get("lab_order") or getattr(self.instance, "lab_order", None)

#         if discount < 0:
#             raise serializers.ValidationError({"discount": "Discount cannot be negative."})
#         if total_amount < 0:
#             raise serializers.ValidationError({"total_amount": "Total amount cannot be negative."})
#         if discount > total_amount:
#             raise serializers.ValidationError({"discount": "Discount cannot exceed total amount."})

#         if lab_order:
#             has_existing_bill = LabBill.objects.filter(lab_order=lab_order)
#             if self.instance:
#                 has_existing_bill = has_existing_bill.exclude(pk=self.instance.pk)
#             if has_existing_bill.exists():
#                 raise serializers.ValidationError(
#                     {"lab_order": "A bill already exists for this lab order."}
#                 )
#         return attrs

# # ------------------------------
# # Lab Equipment Serializer
# # ------------------------------
# class LabEquipmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabEquipment
#         fields = '__all__'

#     def validate(self, attrs):
#         purchase_date = attrs.get("purchase_date", getattr(self.instance, "purchase_date", None))
#         last_service_date = attrs.get(
#             "last_service_date", getattr(self.instance, "last_service_date", None)
#         )
#         if purchase_date and last_service_date and last_service_date < purchase_date:
#             raise serializers.ValidationError(
#                 {"last_service_date": "Last service date cannot be before purchase date."}
#             )
#         return attrs

# # ------------------------------
# # Lab Maintenance Serializer
# # ------------------------------
# class LabMaintenanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabMaintenance
#         fields = '__all__'

#     def validate(self, attrs):
#         equipment = attrs.get("equipment") or getattr(self.instance, "equipment", None)
#         service_date = attrs.get("service_date", getattr(self.instance, "service_date", None))

#         if equipment and service_date and service_date < equipment.purchase_date:
#             raise serializers.ValidationError(
#                 {"service_date": "Service date cannot be before equipment purchase date."}
#             )
#         return attrs


from rest_framework import serializers
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
# Lab Test Serializer
# ------------------------------
class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = '__all__'

    def validate_test_name(self, value):
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("Test name cannot be empty.")
        exists = LabTest.objects.filter(test_name__iexact=cleaned)
        if self.instance:
            exists = exists.exclude(pk=self.instance.pk)
        if exists.exists():
            raise serializers.ValidationError("Lab test with this name already exists.")
        return cleaned

# ------------------------------
# Lab Order Item Serializer
# ------------------------------
class LabOrderItemSerializer(serializers.ModelSerializer):
    lab_test_name = serializers.ReadOnlyField(source='lab_test.test_name')

    class Meta:
        model = LabOrderItem
        fields = '__all__'

    def validate(self, attrs):
        lab_order = attrs.get('lab_order') or getattr(self.instance, 'lab_order', None)
        lab_test = attrs.get('lab_test') or getattr(self.instance, 'lab_test', None)

        if lab_order and lab_order.status == 'Completed':
            raise serializers.ValidationError({
                "lab_order": "Cannot add items to a completed lab order."
            })

        if lab_order and lab_test:
            duplicate = LabOrderItem.objects.filter(
                lab_order=lab_order,
                lab_test=lab_test
            )
            if self.instance:
                duplicate = duplicate.exclude(pk=self.instance.pk)
            if duplicate.exists():
                raise serializers.ValidationError({
                    "lab_test": "This test is already part of the selected order."
                })
        return attrs

# ------------------------------
# Lab Order Serializer
# ------------------------------
class LabOrderSerializer(serializers.ModelSerializer):
    items = LabOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = LabOrder
        fields = '__all__'

    def validate(self, attrs):
        lab_request = attrs.get("lab_request") or getattr(self.instance, "lab_request", None)
        patient = attrs.get("patient") or getattr(self.instance, "patient", None)

        if lab_request and patient:
            expected_patient = lab_request.consultation.appointment.patient
            if patient.pk != expected_patient.pk:
                raise serializers.ValidationError({
                    "patient": "Patient must match the patient from the linked lab request."
                })
        return attrs

# ------------------------------
# Lab Result Serializer
# ------------------------------
class LabResultSerializer(serializers.ModelSerializer):
    lab_test_name = serializers.ReadOnlyField(source='lab_order_item.lab_test.test_name')
    order_number = serializers.ReadOnlyField(source='lab_order_item.lab_order.order_number')

    class Meta:
        model = LabResult
        fields = '__all__'

    def validate_result_value(self, value):
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("Result value cannot be empty.")
        return cleaned

    def _sync_order_status(self, lab_order):
        all_completed = lab_order.items.exists() and not lab_order.items.filter(labresult__isnull=True).exists()
        new_status = 'Completed' if all_completed else 'Pending'
        if lab_order.status != new_status:
            lab_order.status = new_status
            lab_order.save(update_fields=['status'])
            # Update lab_request as well
            lab_request = lab_order.lab_request
            lab_request.status = new_status
            if new_status == 'Completed':
                from django.utils import timezone
                lab_request.completed_at = timezone.now()
            lab_request.save(update_fields=['status', 'completed_at'])

    def create(self, validated_data):
        result = super().create(validated_data)
        self._sync_order_status(result.lab_order_item.lab_order)
        return result

    def update(self, instance, validated_data):
        result = super().update(instance, validated_data)
        self._sync_order_status(result.lab_order_item.lab_order)
        return result

# ------------------------------
# Lab Bill Serializer
# ------------------------------
class LabBillSerializer(serializers.ModelSerializer):
    lab_order_number = serializers.ReadOnlyField(source='lab_order.order_number')

    class Meta:
        model = LabBill
        fields = '__all__'
        read_only_fields = ['bill_number', 'final_amount', 'created_at']

    def validate(self, attrs):
        total_amount = attrs.get('total_amount', getattr(self.instance, 'total_amount', 0))
        discount = attrs.get('discount', getattr(self.instance, 'discount', 0))
        lab_order = attrs.get('lab_order') or getattr(self.instance, 'lab_order', None)

        if total_amount < 0:
            raise serializers.ValidationError({'total_amount': 'Total amount cannot be negative.'})
        if discount < 0:
            raise serializers.ValidationError({'discount': 'Discount cannot be negative.'})
        if discount > total_amount:
            raise serializers.ValidationError({'discount': 'Discount cannot exceed total amount.'})

        if lab_order:
            existing_bill = LabBill.objects.filter(lab_order=lab_order)
            if self.instance:
                existing_bill = existing_bill.exclude(pk=self.instance.pk)
            if existing_bill.exists():
                raise serializers.ValidationError({'lab_order': 'A bill already exists for this lab order.'})
        return attrs

# ------------------------------
# Lab Equipment Serializer
# ------------------------------
class LabEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabEquipment
        fields = '__all__'

    def validate(self, attrs):
        purchase_date = attrs.get('purchase_date', getattr(self.instance, 'purchase_date', None))
        last_service_date = attrs.get('last_service_date', getattr(self.instance, 'last_service_date', None))
        if purchase_date and last_service_date and last_service_date < purchase_date:
            raise serializers.ValidationError({
                'last_service_date': 'Last service date cannot be before purchase date.'
            })
        return attrs

# ------------------------------
# Lab Maintenance Serializer
# ------------------------------
class LabMaintenanceSerializer(serializers.ModelSerializer):
    equipment_name = serializers.ReadOnlyField(source='equipment.name')

    class Meta:
        model = LabMaintenance
        fields = '__all__'

    def validate(self, attrs):
        equipment = attrs.get('equipment') or getattr(self.instance, 'equipment', None)
        service_date = attrs.get('service_date', getattr(self.instance, 'service_date', None))

        if equipment and service_date and service_date < equipment.purchase_date:
            raise serializers.ValidationError({
                'service_date': 'Service date cannot be before equipment purchase date.'
            })
        return attrs