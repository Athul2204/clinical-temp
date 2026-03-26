from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from authentication.utils import IsDoctor

from reception.models import Appointment
from doctor.models import Consultation, Prescription
from labtechnician.models import LabResult

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
# Helper: Get Logged-in Doctor
# ===============================

def get_logged_in_doctor(request):
    try:
        return request.user.staff_profile.doctor_profile
    except AttributeError:
        return None


# ===============================
# 1️⃣ TODAY APPOINTMENTS
# ===============================

class TodayAppointmentsView(APIView):

    permission_classes = [IsDoctor]

    def get(self, request):

        doctor = get_logged_in_doctor(request)

        if not doctor:
            return Response(
                {"message": "Doctor profile not found"},
                status=status.HTTP_403_FORBIDDEN
            )

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

    permission_classes = [IsDoctor]

    def get(self, request, appointment_id):

        doctor = get_logged_in_doctor(request)

        if not doctor:
            return Response(
                {"message": "Doctor profile not found"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            appointment = Appointment.objects.get(
                appointment_id=appointment_id,
                doctor=doctor  # 🔥 restrict to logged-in doctor
            )
        except Appointment.DoesNotExist:
            return Response(
                {"message": "Appointment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        patient = appointment.patient

        current_consultation = Consultation.objects.filter(
            appointment=appointment
        ).first()

        consultations = Consultation.objects.filter(
            appointment__patient=patient
        ).exclude(
            appointment=appointment
        ).order_by("-created_at")[:3]

        prescriptions = Prescription.objects.filter(
            consultation__appointment__patient=patient
        ).order_by("-created_at")[:3]

        lab_results = LabResult.objects.filter(
            lab_order_item__lab_order__patient=patient
        ).order_by("-created_at")[:3]

        data = {
            "appointment": AppointmentSerializer(appointment).data,
            "patient": PatientDetailSerializer(patient).data,
            "current_consultation":
                PreviousConsultationSerializer(
                    current_consultation
                ).data if current_consultation else None,
            "previous_consultations":
                PreviousConsultationSerializer(
                    consultations,
                    many=True
                ).data,
            "previous_prescriptions":
                PreviousPrescriptionSerializer(
                    prescriptions,
                    many=True
                ).data,
            "lab_results":
                LabResultSerializer(
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

    permission_classes = [IsDoctor]

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

    permission_classes = [IsDoctor]

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

    permission_classes = [IsDoctor]

    def get(self, request, consultation_id):

        try:
            consultation = Consultation.objects.get(id=consultation_id)
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

    permission_classes = [IsDoctor]

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