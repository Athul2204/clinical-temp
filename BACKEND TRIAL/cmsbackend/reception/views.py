# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from django.utils import timezone

# from .models import Patient, Appointment, ConsultationBill
# from administration.models import DoctorProfile

# from .serializers import (
#     PatientSerializer,
#     AppointmentSerializer,
#     ConsultationBillSerializer
# )


# # ===============================
# # 1️⃣ CREATE PATIENT
# # ===============================
# class CreatePatientView(APIView):

#     def post(self, request):

#         serializer = PatientSerializer(data=request.data)

#         if serializer.is_valid():
#             patient = serializer.save()

#             return Response(
#                 {
#                     "message": "Patient created successfully",
#                     "patient_id": patient.patient_id
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ===============================
# # 2️⃣ LIST ALL PATIENTS
# # ===============================
# class PatientListView(APIView):

#     def get(self, request):

#         patients = Patient.objects.all().order_by("-created_at")

#         serializer = PatientSerializer(patients, many=True)

#         return Response(
#             {
#                 "count": patients.count(),
#                 "data": serializer.data
#             }
#         )


# # ===============================
# # 3️⃣ BOOK APPOINTMENT
# # ===============================
# class CreateAppointmentView(APIView):

#     def post(self, request):

#         serializer = AppointmentSerializer(data=request.data)

#         if serializer.is_valid():
#             appointment = serializer.save()

#             return Response(
#                 {
#                     "message": "Appointment booked successfully",
#                     "appointment_id": appointment.appointment_id
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ===============================
# # 4️⃣ GET APPOINTMENTS BY DATE
# # ===============================
# class AppointmentListByDateView(APIView):

#     def get(self, request):

#         date_param = request.query_params.get("date")

#         if not date_param:
#             return Response(
#                 {"error": "Date is required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         appointments = Appointment.objects.filter(
#             appointment_date=date_param
#         ).order_by("token_number")

#         serializer = AppointmentSerializer(appointments, many=True)

#         return Response(
#             {
#                 "count": appointments.count(),
#                 "data": serializer.data
#             }
#         )


# # ===============================
# # 5️⃣ CANCEL APPOINTMENT
# # ===============================
# class CancelAppointmentView(APIView):

#     def patch(self, request, appointment_id):

#         try:
#             appointment = Appointment.objects.get(
#                 appointment_id=appointment_id
#             )
#         except Appointment.DoesNotExist:
#             return Response(
#                 {"error": "Appointment not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         appointment.status = "Cancelled"
#         appointment.save()

#         return Response(
#             {"message": "Appointment cancelled successfully"}
#         )


# # ===============================
# # 6️⃣ GENERATE BILL
# # ===============================
# class CreateBillView(APIView):

#     def post(self, request):

#         serializer = ConsultationBillSerializer(data=request.data)

#         if serializer.is_valid():
#             bill = serializer.save()

#             return Response(
#                 {
#                     "message": "Bill generated successfully",
#                     "bill_id": bill.bill_id
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ===============================
# # 7️⃣ PAY BILL
# # ===============================
# class PayBillView(APIView):

#     def patch(self, request, bill_id):

#         try:
#             bill = ConsultationBill.objects.get(bill_id=bill_id)
#         except ConsultationBill.DoesNotExist:
#             return Response(
#                 {"error": "Bill not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         bill.status = "Paid"
#         bill.save()

#         return Response(
#             {"message": "Bill marked as paid"}
#         )

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from django.utils import timezone

# from .models import Patient, Appointment, ConsultationBill
# from administration.models import DoctorProfile

# from .serializers import (
#     PatientSerializer,
#     AppointmentSerializer,
#     ConsultationBillSerializer
# )


# # ===============================
# # 1️⃣ CREATE PATIENT
# # ===============================
# class CreatePatientView(APIView):

#     def post(self, request):

#         serializer = PatientSerializer(data=request.data)

#         if serializer.is_valid():
#             patient = serializer.save()

#             return Response(
#                 {
#                     "message": "Patient created successfully",
#                     "patient_id": patient.patient_id
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ===============================
# # 2️⃣ LIST ALL PATIENTS
# # ===============================
# class PatientListView(APIView):

#     def get(self, request):

#         patients = Patient.objects.all().order_by("-created_at")

#         serializer = PatientSerializer(patients, many=True)

#         return Response(
#             {
#                 "count": patients.count(),
#                 "data": serializer.data
#             }
#         )


# # ===============================
# # 3️⃣ BOOK APPOINTMENT
# # ===============================
# class CreateAppointmentView(APIView):

#     def post(self, request):

#         serializer = AppointmentSerializer(data=request.data)

#         if serializer.is_valid():
#             appointment = serializer.save()

#             return Response(
#                 {
#                     "message": "Appointment booked successfully",
#                     "appointment_id": appointment.appointment_id
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ===============================
# # 4️⃣ GET APPOINTMENTS BY DATE
# # ===============================
# class AppointmentListByDateView(APIView):

#     def get(self, request):

#         date_param = request.query_params.get("date")

#         if not date_param:
#             return Response(
#                 {"error": "Date is required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         appointments = Appointment.objects.filter(
#             appointment_date=date_param
#         ).order_by("token_number")

#         serializer = AppointmentSerializer(appointments, many=True)

#         return Response(
#             {
#                 "count": appointments.count(),
#                 "data": serializer.data
#             }
#         )


# # ===============================
# # 5️⃣ CANCEL APPOINTMENT
# # ===============================
# class CancelAppointmentView(APIView):

#     def patch(self, request, appointment_id):

#         try:
#             appointment = Appointment.objects.get(
#                 appointment_id=appointment_id
#             )
#         except Appointment.DoesNotExist:
#             return Response(
#                 {"error": "Appointment not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         appointment.status = "Cancelled"
#         appointment.save()

#         return Response(
#             {"message": "Appointment cancelled successfully"}
#         )


# # ===============================
# # 6️⃣ GENERATE BILL
# # ===============================
# class CreateBillView(APIView):

#     def post(self, request):

#         serializer = ConsultationBillSerializer(data=request.data)

#         if serializer.is_valid():
#             bill = serializer.save()

#             return Response(
#                 {
#                     "message": "Bill generated successfully",
#                     "bill_id": bill.bill_id
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ===============================
# # 7️⃣ PAY BILL
# # ===============================
# class PayBillView(APIView):

#     def patch(self, request, bill_id):

#         try:
#             bill = ConsultationBill.objects.get(bill_id=bill_id)
#         except ConsultationBill.DoesNotExist:
#             return Response(
#                 {"error": "Bill not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         bill.status = "Paid"
#         bill.save()

#         return Response(
#             {"message": "Bill marked as paid"}
#         )
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from django.utils import timezone

# from .models import Patient, Appointment, ConsultationBill
# from administration.models import DoctorProfile

# from .serializers import (
#     PatientSerializer,
#     AppointmentSerializer,
#     ConsultationBillSerializer
# )


# # ===============================
# # 1️⃣ CREATE PATIENT
# # ===============================
# class CreatePatientView(APIView):

#     def post(self, request):

#         serializer = PatientSerializer(data=request.data)

#         if serializer.is_valid():
#             patient = serializer.save()

#             return Response(
#                 {
#                     "message": "Patient created successfully",
#                     "patient_id": patient.patient_id
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ===============================
# # 2️⃣ LIST ALL PATIENTS
# # ===============================
# class PatientListView(APIView):

#     def get(self, request):

#         patients = Patient.objects.all().order_by("-created_at")

#         serializer = PatientSerializer(patients, many=True)

#         return Response(
#             {
#                 "count": patients.count(),
#                 "data": serializer.data
#             }
#         )


# # ===============================
# # 3️⃣ BOOK APPOINTMENT
# # ===============================
# class CreateAppointmentView(APIView):

#     def post(self, request):

#         serializer = AppointmentSerializer(data=request.data)

#         if serializer.is_valid():
#             appointment = serializer.save()

#             return Response(
#                 {
#                     "message": "Appointment booked successfully",
#                     "appointment_id": appointment.appointment_id
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ===============================
# # 4️⃣ GET APPOINTMENTS BY DATE
# # ===============================
# class AppointmentListByDateView(APIView):

#     def get(self, request):

#         date_param = request.query_params.get("date")

#         if not date_param:
#             return Response(
#                 {"error": "Date is required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         appointments = Appointment.objects.filter(
#             appointment_date=date_param
#         ).order_by("token_number")

#         serializer = AppointmentSerializer(appointments, many=True)

#         return Response(
#             {
#                 "count": appointments.count(),
#                 "data": serializer.data
#             }
#         )


# # ===============================
# # 5️⃣ CANCEL APPOINTMENT
# # ===============================
# class CancelAppointmentView(APIView):

#     def patch(self, request, appointment_id):

#         try:
#             appointment = Appointment.objects.get(
#                 appointment_id=appointment_id
#             )
#         except Appointment.DoesNotExist:
#             return Response(
#                 {"error": "Appointment not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         appointment.status = "Cancelled"
#         appointment.save()

#         return Response(
#             {"message": "Appointment cancelled successfully"}
#         )


# # ===============================
# # 6️⃣ GENERATE BILL
# # ===============================
# class CreateBillView(APIView):

#     def post(self, request):

#         serializer = ConsultationBillSerializer(data=request.data)

#         if serializer.is_valid():
#             bill = serializer.save()

#             return Response(
#                 {
#                     "message": "Bill generated successfully",
#                     "bill_id": bill.bill_id
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ===============================
# # 7️⃣ PAY BILL
# # ===============================
# class PayBillView(APIView):

#     def patch(self, request, bill_id):

#         try:
#             bill = ConsultationBill.objects.get(bill_id=bill_id)
#         except ConsultationBill.DoesNotExist:
#             return Response(
#                 {"error": "Bill not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         bill.status = "Paid"
#         bill.save()

#         return Response(
#             {"message": "Bill marked as paid"}
#         )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction

from .models import Patient, Appointment, ConsultationBill, DoctorAvailability
from administration.models import DoctorProfile
from .serializers import (
    PatientSerializer,
    AppointmentSerializer,
    ConsultationBillSerializer,
    DoctorAvailabilitySerializer,
)


# ===============================
# 1️⃣ CREATE PATIENT
# ===============================
class CreatePatientView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()
            return Response(
                {"message": "Patient created successfully", "patient_id": patient.patient_id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ===============================
# 2️⃣ LIST ALL PATIENTS
# ===============================
class PatientListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients = Patient.objects.all().order_by("-created_at")
        serializer = PatientSerializer(patients, many=True)
        return Response({"count": patients.count(), "data": serializer.data})


# ===============================
# 3️⃣ BOOK APPOINTMENT
# ===============================
# ✅ BILLING GATE: A new appointment can only be booked if the patient's most
#    recent appointment has a PAID consultation bill (or they have no prior
#    appointments). Enforces: "bill must be cleared before next visit."
class CreateAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        patient_id = request.data.get("patient")

        # ── BILLING GATE ──────────────────────────────────────────────────────
        if patient_id:
            last_appointment = (
                Appointment.objects
                .filter(patient_id=patient_id)
                .exclude(status="Cancelled")
                .order_by("-appointment_id")
                .select_related("bill")
                .first()
            )
            if last_appointment:
                try:
                    bill = last_appointment.bill
                    if bill.status != "Paid":
                        return Response(
                            {
                                "error": (
                                    "Cannot schedule a new appointment. "
                                    "The previous consultation bill is unpaid. "
                                    "Please clear the outstanding bill first."
                                ),
                                "unpaid_bill_id": bill.bill_id,
                                "unpaid_appointment_id": last_appointment.appointment_id,
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                except ConsultationBill.DoesNotExist:
                    return Response(
                        {
                            "error": (
                                "Cannot schedule a new appointment. "
                                "The previous appointment has no consultation bill. "
                                "Please complete billing for that appointment first."
                            ),
                            "unpaid_appointment_id": last_appointment.appointment_id,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        # ─────────────────────────────────────────────────────────────────────

        try:
            appointment = serializer.save()
            return Response(
                {
                    "message": "Appointment booked successfully",
                    "appointment_id": appointment.appointment_id,
                    "token_number": appointment.token_number,
                    "consultation_fee": appointment.consultation_fee,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ===============================
# 4️⃣ GET APPOINTMENTS — flexible filter
# ===============================
# ✅ FIX: Supports ?date=, ?patient=, and ?appointment_id= filters.
class AppointmentListByDateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_param           = request.query_params.get("date")
        patient_param        = request.query_params.get("patient")
        appointment_id_param = request.query_params.get("appointment_id")

        if not any([date_param, patient_param, appointment_id_param]):
            return Response(
                {"error": "At least one filter is required: date, patient, or appointment_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        qs = Appointment.objects.select_related("patient", "doctor__staff", "bill").all()

        if date_param:
            qs = qs.filter(appointment_date=date_param)
        if patient_param:
            qs = qs.filter(patient__patient_id=patient_param)
        if appointment_id_param:
            qs = qs.filter(appointment_id=appointment_id_param)

        qs = qs.order_by("token_number")
        serializer = AppointmentSerializer(qs, many=True)
        return Response({"count": qs.count(), "data": serializer.data})


# ===============================
# 5️⃣ CANCEL APPOINTMENT
# ===============================
class CancelAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def patch(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(appointment_id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

        if appointment.status == "Cancelled":
            return Response({"error": "Appointment is already cancelled"}, status=status.HTTP_400_BAD_REQUEST)

        appointment.status = "Cancelled"
        appointment.save()
        return Response({"message": "Appointment cancelled successfully"})


# ===============================
# 6️⃣ GENERATE CONSULTATION BILL
# ===============================
class CreateBillView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = ConsultationBillSerializer(data=request.data)
        if serializer.is_valid():
            bill = serializer.save()
            return Response(
                {"message": "Bill generated successfully", "bill_id": bill.bill_id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ===============================
# 7️⃣ PAY CONSULTATION BILL
# ===============================
class PayBillView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def patch(self, request, bill_id):
        try:
            bill = ConsultationBill.objects.get(bill_id=bill_id)
        except ConsultationBill.DoesNotExist:
            return Response({"error": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)

        if bill.status == "Paid":
            return Response({"error": "Bill is already paid"}, status=status.HTTP_400_BAD_REQUEST)

        bill.status = "Paid"
        bill.save()
        return Response({"message": "Bill marked as paid"})


# ===============================
# 8️⃣ LIST DOCTOR AVAILABILITY
# ===============================
class DoctorAvailabilityListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_param = request.query_params.get("date")
        qs = DoctorAvailability.objects.select_related("doctor__staff").all()
        if date_param:
            qs = qs.filter(available_date=date_param)
        qs = qs.order_by("available_date", "start_time")
        serializer = DoctorAvailabilitySerializer(qs, many=True)
        return Response({"count": qs.count(), "data": serializer.data})


# ================================
# 9️⃣ CREATE DOCTOR AVAILABILITY
# ================================
class CreateDoctorAvailabilityView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = DoctorAvailabilitySerializer(data=request.data)
        if serializer.is_valid():
            slot = serializer.save()
            return Response(
                {"message": "Availability added successfully", "availability_id": slot.availability_id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =================================
# 🔟 DELETE DOCTOR AVAILABILITY
# =================================
class DeleteDoctorAvailabilityView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def delete(self, request, availability_id):
        try:
            slot = DoctorAvailability.objects.get(availability_id=availability_id)
        except DoctorAvailability.DoesNotExist:
            return Response({"error": "Slot not found"}, status=status.HTTP_404_NOT_FOUND)
        slot.delete()
        return Response({"message": "Availability slot removed"}, status=status.HTTP_200_OK)