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



from rest_framework import serializers
from .models import Medicine, MedicineBatch, MedicineStockLog, Dispense, DispenseItem, MedicineBill

# ------------------------------
# Medicine Serializer
# ------------------------------
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

# ------------------------------
# Medicine Batch Serializer
# ------------------------------
class MedicineBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineBatch
        fields = '__all__'

# ------------------------------
# Medicine Stock Log Serializer
# ------------------------------
class MedicineStockLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineStockLog
        fields = '__all__'

# ------------------------------
# Dispense Item Serializer
# ------------------------------
class DispenseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispenseItem
        fields = '__all__'

# ------------------------------
# Dispense Serializer
# ------------------------------
class DispenseSerializer(serializers.ModelSerializer):
    items = DispenseItemSerializer(many=True, read_only=True)

    class Meta:
        model = Dispense
        fields = '__all__'

# ------------------------------
# Medicine Bill Serializer
# ------------------------------
class MedicineBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineBill
        fields = '__all__'