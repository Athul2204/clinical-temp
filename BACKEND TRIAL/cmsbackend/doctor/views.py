# from django.utils import timezone

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from authentication.utils import IsDoctor

# from reception.models import Appointment
# from doctor.models import Consultation, Prescription
# from labtechnician.models import LabResult

# from .serializers import (
#     TodayAppointmentSerializer,
#     PatientDetailSerializer,
#     AppointmentSerializer,
#     PreviousConsultationSerializer,
#     PreviousPrescriptionSerializer,
#     LabResultSerializer,
#     ConsultationCreateSerializer,
#     LabTestRequestSerializer,
#     LabResultViewSerializer,
#     PrescriptionCreateSerializer
# )


# # ===============================
# # Helper: Get Logged-in Doctor
# # ===============================

# def get_logged_in_doctor(request):
#     try:
#         return request.user.staff_profile.doctor_profile
#     except AttributeError:
#         return None


# # ===============================
# # 1️⃣ TODAY APPOINTMENTS
# # ===============================

# class TodayAppointmentsView(APIView):

#     permission_classes = [IsDoctor]

#     def get(self, request):

#         doctor = get_logged_in_doctor(request)

#         if not doctor:
#             return Response(
#                 {"message": "Doctor profile not found"},
#                 status=status.HTTP_403_FORBIDDEN
#             )

#         today = timezone.now().date()

#         appointments = Appointment.objects.filter(
#             doctor=doctor,
#             appointment_date=today
#         ).order_by("token_number")

#         serializer = TodayAppointmentSerializer(appointments, many=True)

#         return Response(
#             {
#                 "message": "Today's appointments fetched successfully",
#                 "count": appointments.count(),
#                 "data": serializer.data
#             },
#             status=status.HTTP_200_OK
#         )


# # ===============================
# # 2️⃣ CONSULTATION PAGE DATA
# # ===============================

# class ConsultationPageView(APIView):

#     permission_classes = [IsDoctor]

#     def get(self, request, appointment_id):

#         doctor = get_logged_in_doctor(request)

#         if not doctor:
#             return Response(
#                 {"message": "Doctor profile not found"},
#                 status=status.HTTP_403_FORBIDDEN
#             )

#         try:
#             appointment = Appointment.objects.get(
#                 appointment_id=appointment_id,
#                 doctor=doctor  # 🔥 restrict to logged-in doctor
#             )
#         except Appointment.DoesNotExist:
#             return Response(
#                 {"message": "Appointment not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         patient = appointment.patient

#         current_consultation = Consultation.objects.filter(
#             appointment=appointment
#         ).first()

#         consultations = Consultation.objects.filter(
#             appointment__patient=patient
#         ).exclude(
#             appointment=appointment
#         ).order_by("-created_at")[:3]

#         prescriptions = Prescription.objects.filter(
#             consultation__appointment__patient=patient
#         ).order_by("-created_at")[:3]

#         lab_results = LabResult.objects.filter(
#             lab_order_item__lab_order__patient=patient
#         ).order_by("-created_at")[:3]

#         data = {
#             "appointment": AppointmentSerializer(appointment).data,
#             "patient": PatientDetailSerializer(patient).data,
#             "current_consultation":
#                 PreviousConsultationSerializer(
#                     current_consultation
#                 ).data if current_consultation else None,
#             "previous_consultations":
#                 PreviousConsultationSerializer(
#                     consultations,
#                     many=True
#                 ).data,
#             "previous_prescriptions":
#                 PreviousPrescriptionSerializer(
#                     prescriptions,
#                     many=True
#                 ).data,
#             "lab_results":
#                 LabResultSerializer(
#                     lab_results,
#                     many=True
#                 ).data
#         }

#         return Response(
#             {
#                 "message": "Consultation page data fetched successfully",
#                 "data": data
#             },
#             status=status.HTTP_200_OK
#         )


# # ===============================
# # 3️⃣ CREATE CONSULTATION
# # ===============================

# class CreateConsultationView(APIView):

#     permission_classes = [IsDoctor]

#     def post(self, request):

#         serializer = ConsultationCreateSerializer(
#             data=request.data,
#             context={"request": request}
#         )

#         if serializer.is_valid():
#             consultation = serializer.save()

#             return Response(
#                 {
#                     "message": "Consultation created successfully",
#                     "consultation_code": consultation.consultation_code
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


# # ===============================
# # 4️⃣ CREATE LAB TEST REQUEST
# # ===============================

# class CreateLabTestRequestView(APIView):

#     permission_classes = [IsDoctor]

#     def post(self, request):

#         serializer = LabTestRequestSerializer(
#             data=request.data,
#             context={"request": request}
#         )

#         if serializer.is_valid():
#             lab_request = serializer.save()

#             return Response(
#                 {
#                     "message": "Lab test request created successfully",
#                     "lab_request_id": lab_request.id
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


# # ===============================
# # 5️⃣ VIEW LAB RESULTS
# # ===============================

# class ViewLabResults(APIView):

#     permission_classes = [IsDoctor]

#     def get(self, request, consultation_id):

#         try:
#             consultation = Consultation.objects.get(id=consultation_id)
#         except Consultation.DoesNotExist:
#             return Response(
#                 {"message": "Consultation not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         lab_results = LabResult.objects.filter(
#             lab_order_item__lab_order__lab_request__consultation=consultation
#         )

#         serializer = LabResultViewSerializer(
#             lab_results,
#             many=True
#         )

#         return Response(
#             {
#                 "message": "Lab results fetched successfully",
#                 "results": serializer.data
#             },
#             status=status.HTTP_200_OK
#         )


# # ===============================
# # 6️⃣ CREATE PRESCRIPTION
# # ===============================

# class CreatePrescriptionView(APIView):

#     permission_classes = [IsDoctor]

#     def post(self, request):

#         serializer = PrescriptionCreateSerializer(
#             data=request.data,
#             context={"request": request}
#         )

#         if serializer.is_valid():
#             prescription = serializer.save()

#             return Response(
#                 {
#                     "message": "Prescription created successfully",
#                     "prescription_code": prescription.prescription_code
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission

from reception.models import Appointment
from doctor.models import Consultation, Prescription, LabTestRequest
from labtechnician.models import LabResult

from .serializers import (
    TodayAppointmentSerializer,
    PatientDetailSerializer,
    AppointmentSerializer,
    PreviousConsultationSerializer,
    PreviousPrescriptionSerializer,
    ConsultationCreateSerializer,
    LabTestRequestSerializer,
    LabResultViewSerializer,
    PrescriptionCreateSerializer,
)


# ===============================
# Custom Permission: Doctor Only
# ===============================
class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.staff_profile.role == "Doctor"
        except AttributeError:
            return False


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
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
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
                doctor=doctor
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

        previous_consultations = Consultation.objects.filter(
            appointment__patient=patient
        ).exclude(
            appointment=appointment
        ).order_by("-created_at")[:3]

        previous_prescriptions = Prescription.objects.filter(
            consultation__appointment__patient=patient
        ).order_by("-created_at")[:3]

        # ✅ Scope lab_results strictly to the CURRENT consultation's lab request.
        # Also expose results_viewed so the frontend can show the "Mark Viewed" button.
        lab_results = []
        lab_results_viewed = False
        lab_request_id = None

        if current_consultation:
            lab_request = getattr(current_consultation, "lab_request", None)
            if lab_request:
                lab_request_id = lab_request.id
                lab_results_viewed = lab_request.results_viewed
                current_lab_results = LabResult.objects.filter(
                    lab_order_item__lab_order__lab_request=lab_request
                ).order_by("-created_at")
                lab_results = LabResultViewSerializer(
                    current_lab_results, many=True
                ).data

        data = {
            "appointment": AppointmentSerializer(appointment).data,
            "patient": PatientDetailSerializer(patient).data,
            "current_consultation": (
                PreviousConsultationSerializer(current_consultation).data
                if current_consultation
                else None
            ),
            "previous_consultations": PreviousConsultationSerializer(
                previous_consultations, many=True
            ).data,
            "previous_prescriptions": PreviousPrescriptionSerializer(
                previous_prescriptions, many=True
            ).data,
            "lab_results": lab_results,
            # ✅ NEW: expose viewed state and lab_request_id for frontend button
            "lab_results_viewed": lab_results_viewed,
            "lab_request_id": lab_request_id,
        }

        return Response(
            {
                "message": "Consultation page data fetched successfully",
                "data": data,
            },
            status=status.HTTP_200_OK,
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
                    "consultation_code": consultation.consultation_code,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                    "lab_request_id": lab_request.id,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        serializer = LabResultViewSerializer(lab_results, many=True)
        return Response(
            {
                "message": "Lab results fetched successfully",
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ===============================
# 6️⃣ MARK LAB RESULTS AS VIEWED
# ===============================
class MarkLabResultsViewedView(APIView):
    """
    POST /api/doctor/lab-results/<lab_request_id>/mark-viewed/
    Doctor explicitly acknowledges they have reviewed the lab results.
    Sets results_viewed=True and stamps results_viewed_at timestamp.
    """
    permission_classes = [IsDoctor]

    def post(self, request, lab_request_id):
        doctor = get_logged_in_doctor(request)
        if not doctor:
            return Response(
                {"message": "Doctor profile not found"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            lab_request = LabTestRequest.objects.select_related(
                "consultation__appointment"
            ).get(id=lab_request_id)
        except LabTestRequest.DoesNotExist:
            return Response(
                {"message": "Lab request not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Ensure this lab request belongs to the logged-in doctor
        if lab_request.doctor != doctor:
            return Response(
                {"message": "Not authorised to mark this lab request"},
                status=status.HTTP_403_FORBIDDEN
            )

        if lab_request.results_viewed:
            return Response(
                {
                    "message": "Lab results already marked as viewed",
                    "results_viewed": True,
                    "results_viewed_at": lab_request.results_viewed_at,
                },
                status=status.HTTP_200_OK,
            )

        # Mark as viewed
        lab_request.results_viewed = True
        lab_request.results_viewed_at = timezone.now()
        lab_request.save(update_fields=["results_viewed", "results_viewed_at"])

        return Response(
            {
                "message": "Lab results marked as viewed successfully",
                "results_viewed": True,
                "results_viewed_at": lab_request.results_viewed_at,
            },
            status=status.HTTP_200_OK,
        )


# ===============================
# 7️⃣ COMPLETE CONSULTATION
# ===============================
class CompleteConsultationView(APIView):
    """
    PATCH /api/doctor/consultation/<appointment_id>/complete/
    Doctor manually marks a consultation as Completed.
    Requirements:
      - A consultation must exist for the appointment.
      - A prescription must have been written for that consultation.
    """
    permission_classes = [IsDoctor]

    def patch(self, request, appointment_id):
        doctor = get_logged_in_doctor(request)
        if not doctor:
            return Response(
                {"message": "Doctor profile not found"},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            appointment = Appointment.objects.get(
                appointment_id=appointment_id,
                doctor=doctor,
            )
        except Appointment.DoesNotExist:
            return Response(
                {"message": "Appointment not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if appointment.status == "Completed":
            return Response(
                {"message": "Consultation is already completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        consultation = Consultation.objects.filter(appointment=appointment).first()
        if not consultation:
            return Response(
                {"message": "No consultation found. Please add a consultation first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        has_prescription = Prescription.objects.filter(
            consultation=consultation
        ).exists()
        if not has_prescription:
            return Response(
                {"message": "Please write a prescription before completing this consultation."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = "Completed"
        appointment.save(update_fields=["status"])

        return Response(
            {"message": "Consultation marked as Completed successfully."},
            status=status.HTTP_200_OK,
        )


# ===============================
# 8️⃣ CREATE PRESCRIPTION
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
                    "prescription_code": prescription.prescription_code,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)