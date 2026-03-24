from django.shortcuts import render
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser  # ✅ NEW

from .models import (
    StaffProfile,
    DoctorProfile,
    ReceptionistProfile,
    LabTechnicianProfile,
    PharmacistProfile,
    AuditLog
)

from .serializers import (
    StaffProfileSerializer,
    DoctorProfileSerializer,
    ReceptionistProfileSerializer,
    LabTechnicianProfileSerializer,
    PharmacistProfileSerializer,
    AuditLogSerializer
)

# =====================================
# 🔐 BASE ADMIN VIEW (JWT + ADMIN ONLY)
# =====================================

class AdminBaseView(APIView):
    permission_classes = [IsAdminUser]


# =====================================
# 1️⃣ STAFF LIST
# =====================================

class StaffListView(AdminBaseView):

    def get(self, request):
        staff = StaffProfile.objects.all()
        serializer = StaffProfileSerializer(staff, many=True)

        return Response({
            "message": "Staff list fetched successfully",
            "count": staff.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# =====================================
# 2️⃣ CREATE STAFF
# =====================================

class CreateStaffView(AdminBaseView):

    def post(self, request):
        serializer = StaffProfileSerializer(data=request.data)

        if serializer.is_valid():
            staff = serializer.save()
            return Response({
                "message": "Staff created successfully",
                "staff_id": staff.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =====================================
# 3️⃣ DOCTOR LIST
# =====================================

class DoctorListView(AdminBaseView):

    def get(self, request):
        doctors = DoctorProfile.objects.all()
        serializer = DoctorProfileSerializer(doctors, many=True)

        return Response({
            "message": "Doctor list fetched successfully",
            "count": doctors.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# =====================================
# 4️⃣ CREATE DOCTOR
# =====================================

class CreateDoctorView(AdminBaseView):

    def post(self, request):
        serializer = DoctorProfileSerializer(data=request.data)

        if serializer.is_valid():
            doctor = serializer.save()
            return Response({
                "message": "Doctor created successfully",
                "doctor_id": doctor.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =====================================
# 5️⃣ RECEPTIONIST LIST
# =====================================

class ReceptionistListView(AdminBaseView):

    def get(self, request):
        receptionists = ReceptionistProfile.objects.all()
        serializer = ReceptionistProfileSerializer(receptionists, many=True)

        return Response({
            "message": "Receptionist list fetched successfully",
            "count": receptionists.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# =====================================
# 6️⃣ CREATE RECEPTIONIST
# =====================================

class CreateReceptionistView(AdminBaseView):

    def post(self, request):
        serializer = ReceptionistProfileSerializer(data=request.data)

        if serializer.is_valid():
            receptionist = serializer.save()
            return Response({
                "message": "Receptionist created successfully",
                "receptionist_id": receptionist.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =====================================
# 7️⃣ LAB TECHNICIAN LIST
# =====================================

class LabTechnicianListView(AdminBaseView):

    def get(self, request):
        technicians = LabTechnicianProfile.objects.all()
        serializer = LabTechnicianProfileSerializer(technicians, many=True)

        return Response({
            "message": "Lab technicians fetched successfully",
            "count": technicians.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# =====================================
# 8️⃣ CREATE LAB TECHNICIAN
# =====================================

class CreateLabTechnicianView(AdminBaseView):

    def post(self, request):
        serializer = LabTechnicianProfileSerializer(data=request.data)

        if serializer.is_valid():
            technician = serializer.save()
            return Response({
                "message": "Lab technician created successfully",
                "technician_id": technician.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =====================================
# 9️⃣ PHARMACIST LIST
# =====================================

class PharmacistListView(AdminBaseView):

    def get(self, request):
        pharmacists = PharmacistProfile.objects.all()
        serializer = PharmacistProfileSerializer(pharmacists, many=True)

        return Response({
            "message": "Pharmacist list fetched successfully",
            "count": pharmacists.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# =====================================
# 🔟 CREATE PHARMACIST
# =====================================

class CreatePharmacistView(AdminBaseView):

    def post(self, request):
        serializer = PharmacistProfileSerializer(data=request.data)

        if serializer.is_valid():
            pharmacist = serializer.save()
            return Response({
                "message": "Pharmacist created successfully",
                "pharmacist_id": pharmacist.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =====================================
# 1️⃣1️⃣ AUDIT LOG LIST
# =====================================

class AuditLogListView(AdminBaseView):

    def get(self, request):
        logs = AuditLog.objects.all().order_by("-timestamp")
        serializer = AuditLogSerializer(logs, many=True)

        return Response({
            "message": "Audit logs fetched successfully",
            "count": logs.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)