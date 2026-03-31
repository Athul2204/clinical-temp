from rest_framework import serializers
from django.utils import timezone
from .models import Patient, Appointment, DoctorAvailability, ConsultationBill
from administration.models import DoctorProfile


# ------------------------------
# Patient Serializer
# ------------------------------
class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Patient
        fields = "__all__"

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits")
        if len(value) != 10:
            raise serializers.ValidationError("Phone number must contain exactly 10 digits")
        return value

    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("First name cannot be empty")
        return value

    def validate_last_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Last name cannot be empty")
        return value


# ------------------------------
# Doctor Availability Serializer
# ------------------------------
class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    doctor_name = serializers.SerializerMethodField(read_only=True)
    doctor_specialization = serializers.CharField(source="doctor.specialization", read_only=True)
    doctor_fee = serializers.IntegerField(source="doctor.consultation_fee", read_only=True)
    doctor_experience = serializers.IntegerField(source="doctor.experience_years", read_only=True)

    class Meta:
        model = DoctorAvailability
        fields = "__all__"

    def get_doctor_name(self, obj):
        try:
            staff = obj.doctor.staff
            full = f"{staff.user.first_name} {staff.user.last_name}".strip()
            return full if full else staff.staff_code
        except Exception:
            return f"Doctor #{obj.doctor_id}"

    def validate(self, data):
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        available_date = data.get("available_date")

        if start_time >= end_time:
            raise serializers.ValidationError("Start time must be earlier than end time")

        if available_date < timezone.now().date():
            raise serializers.ValidationError("Availability date cannot be in the past")

        return data


# ------------------------------
# Nested Bill Serializer (safe - used inside AppointmentSerializer)
# ------------------------------
class NestedBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationBill
        fields = ['bill_id', 'status', 'amount', 'created_at']


# ------------------------------
# Appointment Serializer
# ------------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.first_name", read_only=True)
    patient_full_name = serializers.SerializerMethodField(read_only=True)
    doctor_name = serializers.SerializerMethodField(read_only=True)

    # FIX: Use SerializerMethodField so a missing bill (DoesNotExist) returns null
    # instead of crashing the entire serializer with RelatedObjectDoesNotExist
    bill = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ['token_number', 'consultation_fee', 'created_at']

    def get_patient_full_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"

    def get_doctor_name(self, obj):
        # FIX: StaffProfile has no get_full_name() method - use user fields directly
        try:
            staff = obj.doctor.staff
            full = f"{staff.user.first_name} {staff.user.last_name}".strip()
            return full if full else staff.staff_code
        except Exception:
            return f"Doctor #{obj.doctor_id}"

    def get_bill(self, obj):
        # FIX: safely return None if no bill exists yet (signal may not have run)
        try:
            bill = obj.bill
            return NestedBillSerializer(bill).data
        except Exception:
            return None

    def validate(self, data):
        doctor = data.get("doctor")
        date = data.get("appointment_date")
        time = data.get("appointment_time")

        if not doctor or not date or not time:
            return data

        availability = DoctorAvailability.objects.filter(
            doctor=doctor,
            available_date=date,
            start_time__lte=time,
            end_time__gt=time
        ).exists()

        if not availability:
            raise serializers.ValidationError(
                {"non_field_errors": "Doctor is not available at this date/time"}
            )

        return data


# ------------------------------
# Consultation Bill Serializer
# ------------------------------
class ConsultationBillSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = ConsultationBill
        fields = "__all__"
        read_only_fields = ['amount', 'created_at']

    def get_patient_name(self, obj):
        return f"{obj.appointment.patient.first_name} {obj.appointment.patient.last_name}"

    def get_doctor_name(self, obj):
        # FIX: StaffProfile has no get_full_name() - use user fields directly
        try:
            staff = obj.appointment.doctor.staff
            full = f"{staff.user.first_name} {staff.user.last_name}".strip()
            return full if full else staff.staff_code
        except Exception:
            return "Unknown Doctor"

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount cannot be negative")
        return value