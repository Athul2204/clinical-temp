# from rest_framework import serializers
# from .models import (
#     Patient, Appointment,
#     DoctorAvailability, ConsultationBill
# )
# from administration.models import DoctorProfile


# class PatientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Patient
#         fields = "__all__"


# class DoctorAvailabilitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DoctorAvailability
#         fields = "__all__"


# class AppointmentSerializer(serializers.ModelSerializer):
#     patient = PatientSerializer(read_only=True)
#     doctor = serializers.PrimaryKeyRelatedField(
#         queryset=DoctorProfile.objects.all()
#     )

#     class Meta:
#         model = Appointment
#         fields = "__all__"


# class ConsultationBillSerializer(serializers.ModelSerializer):
#     appointment = AppointmentSerializer(read_only=True)

#     class Meta:
#         model = ConsultationBill
#         fields = "__all__"



from rest_framework import serializers
from .models import Patient, Appointment, DoctorAvailability, ConsultationBill
from datetime import date

# ------------------------------
# Patient Serializer
# ------------------------------
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

    def validate_date_of_birth(self, value):
        today = date.today()
        if value > today:
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

# ------------------------------
# Doctor Availability Serializer
# ------------------------------
class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = '__all__'

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")
        return data

# ------------------------------
# Appointment Serializer
# ------------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):
        # Check doctor availability for that time
        doctor = data['doctor']
        date_ = data['appointment_date']
        time_ = data['appointment_time']
        from .models import DoctorAvailability
        if not DoctorAvailability.objects.filter(doctor=doctor, available_date=date_,
                                                start_time__lte=time_, end_time__gte=time_).exists():
            raise serializers.ValidationError("Doctor is not available at this time.")
        return data

# ------------------------------
# Consultation Bill Serializer
# ------------------------------
class ConsultationBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationBill
        fields = '__all__'

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value