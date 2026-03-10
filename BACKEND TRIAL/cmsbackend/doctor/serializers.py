from rest_framework import serializers
from reception.models import Appointment, Patient
from doctor.models import Consultation, Prescription,LabTestRequest, LabTestRequestItem, PrescriptionItem
from labtechnician.models import LabResult,LabTest
from django.utils import timezone
from django.db import transaction
from pharmacist.models import Medicine
from administration.models import DoctorProfile



class PatientBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "patient_id",
            "first_name",
            "last_name",
            "gender",
            "age"
        ]


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



# -------------------------
# Patient Serializer
# -------------------------
class PatientDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = [
            "patient_id",
            "first_name",
            "last_name",
            "age",
            "gender",
            "blood_group",
            "phone",
            "membership_status"
        ]


# -------------------------
# Appointment Serializer
# -------------------------
class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = [
            "appointment_id",
            "appointment_date",
            "appointment_time",
            "token_number",
            "reason",
            "status"
        ]


# -------------------------
# Previous Consultation
# -------------------------
class PreviousConsultationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consultation
        fields = [
            "consultation_code",
            "symptoms",
            "diagnosis",
            "vitals",
            "advice",
            "created_at"
        ]


# -------------------------
# Previous Prescription
# -------------------------
class PreviousPrescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prescription
        fields = [
            "prescription_code",
            "status",
            "created_at"
        ]


# -------------------------
# Lab Result Serializer
# -------------------------
class LabResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = LabResult
        fields = [
            "result_id",
            "result_value",
            "remarks",
            "is_critical",
            "created_at"
        ]



class ConsultationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consultation
        fields = [
            "appointment",
            "symptoms",
            "diagnosis",
            "vitals",
            "advice"
        ]

    # --------------------------
    # Field Level Validations
    # --------------------------

    def validate_symptoms(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Symptoms cannot be empty"
            )

        if len(value) < 5:
            raise serializers.ValidationError(
                "Symptoms must contain at least 5 characters"
            )

        return value


    def validate_diagnosis(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Diagnosis cannot be empty"
            )

        if len(value) < 3:
            raise serializers.ValidationError(
                "Diagnosis must contain at least 3 characters"
            )

        return value


    def validate_vitals(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Vitals information cannot be empty"
            )

        if len(value) < 3:
            raise serializers.ValidationError(
                "Vitals information is too short"
            )

        return value


    # --------------------------
    # Object Level Validation
    # --------------------------

    def validate(self, data):

        appointment = data.get("appointment")

        # appointment cancelled check
        if appointment.status == "Cancelled":
            raise serializers.ValidationError(
                "Cannot create consultation for cancelled appointment"
            )

        # appointment date validation
        if appointment.appointment_date != timezone.now().date():
            raise serializers.ValidationError(
                "Consultation allowed only for today's appointment"
            )

        # consultation already exists
        if Consultation.objects.filter(
                appointment=appointment
        ).exists():
            raise serializers.ValidationError(
                "Consultation already created for this appointment"
            )

        return data


    # --------------------------
    # Custom Create Method
    # --------------------------

    def create(self, validated_data):

        consultation = Consultation.objects.create(**validated_data)

        return consultation
    


# ----------------------------
# Lab Test Item Serializer
# ----------------------------
class LabTestRequestItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = LabTestRequestItem
        fields = ["lab_test"]

    def validate_lab_test(self, value):

        if not LabTest.objects.filter(test_id=value.test_id).exists():
            raise serializers.ValidationError(
                "Selected lab test does not exist"
            )

        return value


# ----------------------------
# Lab Test Request Serializer
# ----------------------------
class LabTestRequestSerializer(serializers.ModelSerializer):

    tests = LabTestRequestItemSerializer(many=True)

    class Meta:
        model = LabTestRequest
        fields = [
            "consultation",
            "doctor",
            "notes",
            "tests"
        ]


    # ----------------------------
    # Field Validation
    # ----------------------------
    def validate_notes(self, value):

        if value and len(value) < 5:
            raise serializers.ValidationError(
                "Notes must contain at least 5 characters"
            )

        return value


    # ----------------------------
    # Object Validation
    # ----------------------------
    def validate(self, data):

        consultation = data.get("consultation")
        doctor = data.get("doctor")

        # doctor mismatch check
        if consultation.appointment.doctor != doctor:
            raise serializers.ValidationError(
                "Doctor mismatch with consultation"
            )

        # lab request already exists
        if LabTestRequest.objects.filter(
            consultation=consultation
        ).exists():
            raise serializers.ValidationError(
                "Lab request already exists for this consultation"
            )

        tests = self.initial_data.get("tests")

        if not tests:
            raise serializers.ValidationError(
                "At least one lab test must be selected"
            )

        return data


    # ----------------------------
    # Custom Create
    # ----------------------------
    @transaction.atomic
    def create(self, validated_data):

        tests_data = validated_data.pop("tests")

        lab_request = LabTestRequest.objects.create(**validated_data)

        for test in tests_data:
            LabTestRequestItem.objects.create(
                lab_request=lab_request,
                lab_test=test["lab_test"]
            )

        return lab_request




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
            "created_at"
        ] 




# ---------------------------------
# Prescription Item Serializer
# ---------------------------------
class PrescriptionItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrescriptionItem
        fields = [
            "medicine_name",
            "dosage",
            "frequency",
            "duration",
            "instructions"
        ]

    # Field validations
    def validate_duration(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Duration must be greater than zero"
            )

        return value

    def validate_medicine_name(self, value):

        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Medicine name too short"
            )

        return value


# ---------------------------------
# Prescription Serializer
# ---------------------------------
class PrescriptionCreateSerializer(serializers.ModelSerializer):

    items = PrescriptionItemSerializer(many=True)

    class Meta:
        model = Prescription
        fields = [
            "consultation",
            "doctor",
            "items"
        ]


    # -------------------------
    # Object Validation
    # -------------------------
    def validate(self, data):

        consultation = data.get("consultation")
        doctor = data.get("doctor")

        # doctor mismatch
        if consultation.appointment.doctor != doctor:
            raise serializers.ValidationError(
                "Doctor mismatch with consultation"
            )

        # prescription already exists
        if Prescription.objects.filter(
            consultation=consultation
        ).exists():
            raise serializers.ValidationError(
                "Prescription already exists for this consultation"
            )

        # check pending lab tests
        lab_request = getattr(consultation, "lab_request", None)

        if lab_request and lab_request.status == "Pending":
            raise serializers.ValidationError(
                "Cannot prescribe medicines while lab tests are pending"
            )

        items = self.initial_data.get("items")

        if not items:
            raise serializers.ValidationError(
                "At least one medicine must be added"
            )

        return data


    # -------------------------
    # Custom Create
    # -------------------------
    @transaction.atomic
    def create(self, validated_data):

        items_data = validated_data.pop("items")

        prescription = Prescription.objects.create(**validated_data)

        for item in items_data:

            PrescriptionItem.objects.create(
                prescription=prescription,
                medicine_name=item["medicine_name"],
                dosage=item["dosage"],
                frequency=item["frequency"],
                duration=item["duration"],
                instructions=item.get("instructions", "")
            )

        return prescription