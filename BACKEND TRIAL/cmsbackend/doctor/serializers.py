from rest_framework import serializers
from reception.models import Appointment, Patient
from doctor.models import (
    Consultation,
    Prescription,
    LabTestRequest,
    LabTestRequestItem,
    PrescriptionItem
)
from labtechnician.models import LabResult, LabTest
from django.utils import timezone
from django.db import transaction
from pharmacist.models import Medicine
from administration.models import DoctorProfile


# -------------------------
# BASIC SERIALIZERS
# -------------------------

class PatientBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["patient_id", "first_name", "last_name", "gender", "age"]


class TodayAppointmentSerializer(serializers.ModelSerializer):
    patient = PatientBasicSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "appointment_id",
            "patient",
            "appointment_time",
            "token_number",
            "reason",
            "status",
        ]
        read_only_fields = fields


class PatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "patient_id",
            "first_name",
            "last_name",
            "age",
            "gender",
            "email",
            "phone",
            "date_of_birth",
            "blood_group",
            "address",
            "membership_status",
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "appointment_id",
            "doctor",
            "appointment_date",
            "appointment_time",
            "token_number",
            "reason",
            "status",
        ]


# -------------------------
# CONSULTATION
# -------------------------

class PreviousConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = [
            "id",
            "consultation_code",
            "symptoms",
            "diagnosis",
            "vitals",
            "advice",
            "created_at",
        ]


class ConsultationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consultation
        fields = ["appointment", "symptoms", "diagnosis", "vitals", "advice"]

    def validate_symptoms(self, value):
        if not value.strip():
            raise serializers.ValidationError("Symptoms cannot be empty")
        if len(value) < 5:
            raise serializers.ValidationError("Symptoms too short")
        return value

    def validate_diagnosis(self, value):
        if not value.strip():
            raise serializers.ValidationError("Diagnosis cannot be empty")
        if len(value) < 3:
            raise serializers.ValidationError("Diagnosis too short")
        return value

    def validate_vitals(self, value):
        if not value.strip():
            raise serializers.ValidationError("Vitals cannot be empty")
        return value

    def validate(self, data):
        appointment = data.get("appointment")

        if not appointment:
            raise serializers.ValidationError("Appointment is required")

        if appointment.status == "Cancelled":
            raise serializers.ValidationError("Cancelled appointment")

        if appointment.appointment_date != timezone.now().date():
            raise serializers.ValidationError("Only today's consultation allowed")

        if Consultation.objects.filter(appointment=appointment).exists():
            raise serializers.ValidationError("Consultation already exists")

        return data


# -------------------------
# PRESCRIPTION ITEMS
# -------------------------

class PrescriptionItemSerializer(serializers.ModelSerializer):

    medicine_display = serializers.CharField(
        source="medicine_name.name",
        read_only=True
    )

    class Meta:
        model = PrescriptionItem
        fields = [
            "medicine_name",
            "medicine_display",
            "dosage",
            "frequency",
            "duration",
            "instructions",
        ]

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be positive")
        return value


# -------------------------
# PRESCRIPTION
# -------------------------

class PreviousPrescriptionSerializer(serializers.ModelSerializer):
    items = PrescriptionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = ["prescription_code", "status", "created_at", "items"]


class PrescriptionCreateSerializer(serializers.ModelSerializer):

    items = PrescriptionItemSerializer(many=True)

    class Meta:
        model = Prescription
        fields = ["consultation", "doctor", "items"]

    def validate(self, data):

        consultation = data.get("consultation")
        doctor = data.get("doctor")

        if not consultation or not doctor:
            raise serializers.ValidationError("Consultation & Doctor required")

        if consultation.appointment.doctor != doctor:
            raise serializers.ValidationError("Doctor mismatch")

        if Prescription.objects.filter(consultation=consultation).exists():
            raise serializers.ValidationError("Prescription already exists")

        # Only block if a lab request exists AND is still Pending.
        lab_request = getattr(consultation, "lab_request", None)
        if lab_request and lab_request.status == "Pending":
            raise serializers.ValidationError(
                "Cannot prescribe while lab tests are still pending. "
                "Please wait for lab results first."
            )

        items = self.initial_data.get("items")
        if not items:
            raise serializers.ValidationError("Add at least one medicine")

        return data

    @transaction.atomic
    def create(self, validated_data):

        items_data = validated_data.pop("items")

        prescription = Prescription.objects.create(**validated_data)

        medicine_set = set()

        for item in items_data:

            med = item["medicine_name"]

            if med in medicine_set:
                raise serializers.ValidationError(
                    "Duplicate medicine not allowed"
                )

            medicine_set.add(med)

            PrescriptionItem.objects.create(
                prescription=prescription,
                medicine_name=med,
                dosage=item["dosage"],
                frequency=item["frequency"],
                duration=item["duration"],
                instructions=item.get("instructions", "")
            )

        # ✅ Send to pharmacy and mark appointment Completed.
        prescription.send_to_pharmacy()

        return prescription


# -------------------------
# LAB TEST REQUEST
# -------------------------

class LabTestRequestItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = LabTestRequestItem
        fields = ["lab_test"]

    def validate_lab_test(self, value):
        if not LabTest.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError("Invalid lab test")
        return value


class LabTestRequestSerializer(serializers.ModelSerializer):

    tests = LabTestRequestItemSerializer(many=True)

    class Meta:
        model = LabTestRequest
        fields = ["consultation", "doctor", "notes", "tests"]

    def validate_notes(self, value):
        if value and len(value) < 5:
            raise serializers.ValidationError("Notes too short")
        return value

    def validate(self, data):

        consultation = data.get("consultation")
        doctor = data.get("doctor")

        if not consultation or not doctor:
            raise serializers.ValidationError("Consultation & Doctor required")

        if consultation.appointment.doctor != doctor:
            raise serializers.ValidationError("Doctor mismatch")

        if LabTestRequest.objects.filter(consultation=consultation).exists():
            raise serializers.ValidationError("Lab request already exists")

        tests = self.initial_data.get("tests")
        if not tests:
            raise serializers.ValidationError("Select at least one test")

        return data

    @transaction.atomic
    def create(self, validated_data):

        tests_data = validated_data.pop("tests")

        lab_request = LabTestRequest.objects.create(**validated_data)

        test_set = set()

        for test in tests_data:

            lab_test = test["lab_test"]

            if lab_test in test_set:
                raise serializers.ValidationError("Duplicate test not allowed")

            test_set.add(lab_test)

            LabTestRequestItem.objects.create(
                lab_request=lab_request,
                lab_test=lab_test
            )

        return lab_request


# -------------------------
# LAB RESULT
# -------------------------

class LabResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = LabResult
        fields = [
            "result_id",
            "result_value",
            "remarks",
            "is_critical",
            "created_at",
        ]


class LabResultViewSerializer(serializers.ModelSerializer):

    test_name = serializers.CharField(
        source="lab_order_item.lab_test.test_name",
        read_only=True
    )

    class Meta:
        model = LabResult
        fields = [
            "result_id",
            "test_name",
            "result_value",
            "remarks",
            "is_critical",
            "created_at",
        ]