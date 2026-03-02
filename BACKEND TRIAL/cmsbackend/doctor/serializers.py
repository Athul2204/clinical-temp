from rest_framework import serializers
from .models import (
    Consultation, Prescription,
    PrescriptionItem, LabTestRequest
)
from reception.serializers import AppointmentSerializer


class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = "__all__"


class ConsultationSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(read_only=True)

    class Meta:
        model = Consultation
        fields = "__all__"


class PrescriptionSerializer(serializers.ModelSerializer):
    items = PrescriptionItemSerializer(many=True)

    class Meta:
        model = Prescription
        fields = "__all__"

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        prescription = Prescription.objects.create(**validated_data)
        for item in items_data:
            PrescriptionItem.objects.create(
                prescription=prescription,
                **item
            )
        return prescription


class LabTestRequestSerializer(serializers.ModelSerializer):
    consultation = ConsultationSerializer(read_only=True)

    class Meta:
        model = LabTestRequest
        fields = "__all__"