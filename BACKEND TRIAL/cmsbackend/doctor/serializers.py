# from rest_framework import serializers
# from .models import (
#     Consultation, Prescription,
#     PrescriptionItem, LabTestRequest
# )
# from reception.serializers import AppointmentSerializer


# class PrescriptionItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PrescriptionItem
#         fields = "__all__"


# class ConsultationSerializer(serializers.ModelSerializer):
#     appointment = AppointmentSerializer(read_only=True)

#     class Meta:
#         model = Consultation
#         fields = "__all__"


# class PrescriptionSerializer(serializers.ModelSerializer):
#     items = PrescriptionItemSerializer(many=True)

#     class Meta:
#         model = Prescription
#         fields = "__all__"

#     def create(self, validated_data):
#         items_data = validated_data.pop("items")
#         prescription = Prescription.objects.create(**validated_data)
#         for item in items_data:
#             PrescriptionItem.objects.create(
#                 prescription=prescription,
#                 **item
#             )
#         return prescription


# class LabTestRequestSerializer(serializers.ModelSerializer):
#     consultation = ConsultationSerializer(read_only=True)

#     class Meta:
#         model = LabTestRequest
#         fields = "__all__"



from rest_framework import serializers
from .models import Consultation, Prescription, PrescriptionItem, LabTestRequest
from reception.models import Appointment

# ------------------------------
# Consultation Serializer
# ------------------------------
class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'

    def validate_appointment(self, value):
        if value.status != 'Scheduled':
            raise serializers.ValidationError("Consultation can only be created for scheduled appointments.")
        return value

# ------------------------------
# Prescription Item Serializer
# ------------------------------
class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = '__all__'

# ------------------------------
# Prescription Serializer
# ------------------------------
class PrescriptionSerializer(serializers.ModelSerializer):
    items = PrescriptionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = '__all__'

# ------------------------------
# Lab Test Request Serializer
# ------------------------------
class LabTestRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTestRequest
        fields = '__all__'