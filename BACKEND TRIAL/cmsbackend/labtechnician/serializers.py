from rest_framework import serializers
from .models import (
    LabTest, LabOrder, LabOrderItem,
    LabResult, LabBill, LabEquipment, LabMaintenance
)


class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = "__all__"


class LabOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabOrderItem
        fields = "__all__"


class LabOrderSerializer(serializers.ModelSerializer):
    items = LabOrderItemSerializer(many=True)

    class Meta:
        model = LabOrder
        fields = "__all__"

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        lab_order = LabOrder.objects.create(**validated_data)
        for item in items_data:
            LabOrderItem.objects.create(
                lab_order=lab_order,
                **item
            )
        return lab_order


class LabResultSerializer(serializers.ModelSerializer):
    lab_order = LabOrderSerializer(read_only=True)

    class Meta:
        model = LabResult
        fields = "__all__"


class LabBillSerializer(serializers.ModelSerializer):
    lab_order = LabOrderSerializer(read_only=True)

    class Meta:
        model = LabBill
        fields = "__all__"


class LabEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabEquipment
        fields = "__all__"


class LabMaintenanceSerializer(serializers.ModelSerializer):
    equipment = LabEquipmentSerializer(read_only=True)

    class Meta:
        model = LabMaintenance
        fields = "__all__"