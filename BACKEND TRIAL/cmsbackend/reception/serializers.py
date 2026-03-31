# from rest_framework import serializers
# from .models import Patient, Appointment, DoctorAvailability, ConsultationBill
# from administration.models import DoctorProfile
# from django.utils import timezone


# class PatientSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Patient
#         fields = "__all__"

#     def validate_phone(self, value):

#         if not value.isdigit():
#             raise serializers.ValidationError(
#             "Phone number must contain only digits"
#         )

#         if len(value) != 10:
#             raise serializers.ValidationError(
#             "Phone number must contain exactly 10 digits"
#         )

#         return value

#     def validate_first_name(self, value):

#         if not value.strip():
#             raise serializers.ValidationError(
#                 "First name cannot be empty"
#             )

#         return value


# class DoctorAvailabilitySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = DoctorAvailability
#         fields = "__all__"

#     def validate(self, data):

#         start_time = data.get("start_time")
#         end_time = data.get("end_time")
#         available_date = data.get("available_date")

#         # start time validation
#         if start_time >= end_time:
#             raise serializers.ValidationError(
#                 "Start time must be earlier than end time"
#             )

#         # past date validation
#         if available_date < timezone.now().date():
#             raise serializers.ValidationError(
#                 "Availability date cannot be in the past"
#             )

#         return data

# class AppointmentSerializer(serializers.ModelSerializer):

#     patient_name = serializers.CharField(
#         source="patient.first_name",
#         read_only=True
#     )

#     doctor = serializers.PrimaryKeyRelatedField(
#         queryset=DoctorProfile.objects.all()
#     )

#     class Meta:
#         model = Appointment
#         fields = "__all__"

#     def validate(self, data):

#         doctor = data.get("doctor")
#         date = data.get("appointment_date")
#         time = data.get("appointment_time")
#         token = data.get("token_number")

#         # Doctor availability check
#         availability = DoctorAvailability.objects.filter(
#             doctor=doctor,
#             available_date=date,
#             start_time__lte=time,
#             end_time__gte=time
#         ).exists()

#         if not availability:
#             raise serializers.ValidationError(
#                 "Doctor is not available at this time"
#             )

#         # Token duplicate check (safe for update)
#         appointment_qs = Appointment.objects.filter(
#             doctor=doctor,
#             appointment_date=date,
#             token_number=token
#         )

#         if self.instance:
#             appointment_qs = appointment_qs.exclude(
#                 pk=self.instance.pk
#             )

#         if appointment_qs.exists():
#             raise serializers.ValidationError(
#                 "Token number already exists for this date"
#             )

#         return data

# class ConsultationBillSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ConsultationBill
#         fields = "__all__"

#     def validate_amount(self, value):

#         if value < 0:
#             raise serializers.ValidationError(
#                 "Amount cannot be negative"
#             )

#         return value


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
    doctor_name = serializers.CharField(source="doctor.staff.get_full_name", read_only=True)

    class Meta:
        model = DoctorAvailability
        fields = "__all__"

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
# Appointment Serializer
# ------------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.first_name", read_only=True)
    patient_full_name = serializers.SerializerMethodField(read_only=True)
    doctor_name = serializers.CharField(source="doctor.staff.get_full_name", read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"

    def get_patient_full_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"

    def validate(self, data):
        doctor = data.get("doctor")
        date = data.get("appointment_date")
        time = data.get("appointment_time")
        token = data.get("token_number")

        # Doctor availability check
        availability = DoctorAvailability.objects.filter(
            doctor=doctor,
            available_date=date,
            start_time__lte=time,
            end_time__gte=time
        ).exists()
        if not availability:
            raise serializers.ValidationError("Doctor is not available at this time")

        # Token duplicate check
        appointment_qs = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=date,
            token_number=token
        )
        if self.instance:
            appointment_qs = appointment_qs.exclude(pk=self.instance.pk)

        if appointment_qs.exists():
            raise serializers.ValidationError("Token number already exists for this date")

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
        return obj.appointment.doctor.staff.get_full_name()

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount cannot be negative")
        return value