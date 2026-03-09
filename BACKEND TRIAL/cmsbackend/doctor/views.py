from django.shortcuts import render
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reception.models import Appointment
from doctor.models import Consultation, Prescription
from labtechnician.models import LabResult
from administration.models import DoctorProfile

from .serializers import (
    TodayAppointmentSerializer,
    PatientDetailSerializer,
    AppointmentSerializer,
    PreviousConsultationSerializer,
    PreviousPrescriptionSerializer,
    LabResultSerializer,
    ConsultationCreateSerializer,
    LabTestRequestSerializer,
    LabResultViewSerializer,
    PrescriptionCreateSerializer
)


# ===============================
# 1️⃣ TODAY APPOINTMENTS
# ===============================

class TodayAppointmentsView(APIView):

    def get(self, request):

        doctor = DoctorProfile.objects.first()
        today = timezone.now().date()

        appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=today
        ).order_by("token_number")

        serializer = TodayAppointmentSerializer(appointments, many=True)

        return Response(
            {
                "message": "Today's appointments fetched successfully",
                "count": appointments.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# ===============================
# 2️⃣ CONSULTATION PAGE DATA
# ===============================

class ConsultationPageView(APIView):

    def get(self, request, appointment_id):

        try:
            appointment = Appointment.objects.get(
                appointment_id=appointment_id
            )

        except Appointment.DoesNotExist:

            return Response(
                {"message": "Appointment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        patient = appointment.patient

        # 🔹 Current consultation (only this appointment)
        current_consultation = Consultation.objects.filter(
            appointment=appointment
        ).first()

        # 🔹 Previous consultations (exclude current appointment)
        consultations = Consultation.objects.filter(
            appointment__patient=patient
        ).exclude(
            appointment=appointment
        ).order_by("-created_at")

        prescriptions = Prescription.objects.filter(
            consultation__appointment__patient=patient
        )

        lab_results = LabResult.objects.filter(
            lab_order_item__lab_order__patient=patient
        )

        data = {

            "appointment": AppointmentSerializer(appointment).data,

            "patient": PatientDetailSerializer(patient).data,

            # ✅ NEW FIELD
            "current_consultation": 
                PreviousConsultationSerializer(
                    current_consultation
                ).data if current_consultation else None,

            "previous_consultations": PreviousConsultationSerializer(
                consultations,
                many=True
            ).data,

            "previous_prescriptions": PreviousPrescriptionSerializer(
                prescriptions,
                many=True
            ).data,

            "lab_results": LabResultSerializer(
                lab_results,
                many=True
            ).data
        }

        return Response(
            {
                "message": "Consultation page data fetched successfully",
                "data": data
            },
            status=status.HTTP_200_OK
        )

# ===============================
# 3️⃣ CREATE CONSULTATION
# ===============================

class CreateConsultationView(APIView):

    def post(self, request):

        serializer = ConsultationCreateSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():

            consultation = serializer.save()

            return Response(
                {
                    "message": "Consultation created successfully",
                    "consultation_code": consultation.consultation_code
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ===============================
# 4️⃣ CREATE LAB TEST REQUEST
# ===============================

class CreateLabTestRequestView(APIView):

    def post(self, request):

        serializer = LabTestRequestSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():

            lab_request = serializer.save()

            return Response(
                {
                    "message": "Lab test request created successfully",
                    "lab_request_id": lab_request.id
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ===============================
# 5️⃣ VIEW LAB RESULTS
# ===============================

class ViewLabResults(APIView):

    def get(self, request, consultation_id):

        try:
            consultation = Consultation.objects.get(
                id=consultation_id
            )

        except Consultation.DoesNotExist:

            return Response(
                {"message": "Consultation not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        lab_results = LabResult.objects.filter(
            lab_order_item__lab_order__lab_request__consultation=consultation
        )

        serializer = LabResultViewSerializer(
            lab_results,
            many=True
        )

        return Response(
            {
                "message": "Lab results fetched successfully",
                "results": serializer.data
            },
            status=status.HTTP_200_OK
        )


# ===============================
# 6️⃣ CREATE PRESCRIPTION
# ===============================

class CreatePrescriptionView(APIView):

    def post(self, request):

        serializer = PrescriptionCreateSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():

            prescription = serializer.save()

            return Response(
                {
                    "message": "Prescription created successfully",
                    "prescription_code": prescription.prescription_code
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
