# from django.shortcuts import get_object_or_404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAdminUser
# from rest_framework.pagination import PageNumberPagination

# from .models import (
#     StaffProfile, DoctorProfile, ReceptionistProfile,
#     LabTechnicianProfile, PharmacistProfile, AuditLog
# )
# from .serializers import (
#     StaffProfileSerializer, DoctorProfileSerializer,
#     ReceptionistProfileSerializer, LabTechnicianProfileSerializer,
#     PharmacistProfileSerializer, AuditLogSerializer
# )

# # ─── BASE CONFIGURATION ──────────────────────────────────────────

# class AdminBaseView(APIView):
#     permission_classes = [IsAdminUser]

# class StandardPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 100

# # ─── REUSABLE LOGIC CLASSES ──────────────────────────────────────

# class ListCreateModelView(AdminBaseView):
#     """
#     Handles Collection actions: 
#     GET -> List all items (with pagination)
#     POST -> Create a new item
#     """
#     model = None
#     serializer_class = None
#     order_field = 'id'

#     def get_queryset(self):
#         return self.model.objects.all().order_by(f'-{self.order_field}')

#     def get(self, request):
#         queryset = self.get_queryset()
#         paginator = StandardPagination()
#         page = paginator.paginate_queryset(queryset, request)
#         serializer = self.serializer_class(page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             instance = serializer.save()
#             return Response({
#                 "message": f"{self.model.__name__} created successfully",
#                 "id": instance.pk,
#                 "data": serializer.data
#             }, status=status.HTTP_201_CREATED)
#         return Response({
#             "message": "Validation failed",
#             "errors": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)


# class RetrieveUpdateDeleteView(AdminBaseView):
#     """
#     Handles Individual Item actions:
#     GET -> Retrieve one
#     PUT -> Full update
#     PATCH -> Partial update
#     DELETE -> Remove item
#     """
#     serializer_class = None

#     def _get_object(self, pk):
#         # Dynamically determine the model from the Serializer's Meta class
#         model = self.serializer_class.Meta.model
#         return get_object_or_404(model, pk=pk)

#     def get(self, request, pk):
#         instance = self._get_object(pk)
#         serializer = self.serializer_class(instance)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         instance = self._get_object(pk)
#         serializer = self.serializer_class(instance, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Updated successfully", "data": serializer.data})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         instance = self._get_object(pk)
#         serializer = self.serializer_class(instance, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Partial update successful", "data": serializer.data})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         instance = self._get_object(pk)
#         instance.delete()
#         return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# # ─── FINAL IMPLEMENTATIONS ───────────────────────────────────────

# # STAFF
# class StaffListView(ListCreateModelView):
#     model = StaffProfile
#     serializer_class = StaffProfileSerializer

# class StaffDetailView(RetrieveUpdateDeleteView):
#     serializer_class = StaffProfileSerializer

# # DOCTOR
# class DoctorListView(ListCreateModelView):
#     model = DoctorProfile
#     serializer_class = DoctorProfileSerializer
#     order_field = 'doctor_id'

# class DoctorDetailView(RetrieveUpdateDeleteView):
#     serializer_class = DoctorProfileSerializer

# # RECEPTIONIST
# class ReceptionistListView(ListCreateModelView):
#     model = ReceptionistProfile
#     serializer_class = ReceptionistProfileSerializer
#     order_field = 'profile_id'

# class ReceptionistDetailView(RetrieveUpdateDeleteView):
#     serializer_class = ReceptionistProfileSerializer

# # LAB TECHNICIAN
# class LabTechnicianListView(ListCreateModelView):
#     model = LabTechnicianProfile
#     serializer_class = LabTechnicianProfileSerializer
#     order_field = 'profile_id'

# class LabTechnicianDetailView(RetrieveUpdateDeleteView):
#     serializer_class = LabTechnicianProfileSerializer

# # PHARMACIST
# class PharmacistListView(ListCreateModelView):
#     model = PharmacistProfile
#     serializer_class = PharmacistProfileSerializer

# class PharmacistDetailView(RetrieveUpdateDeleteView):
#     serializer_class = PharmacistProfileSerializer

# # AUDIT LOG (Read-Only)
# class AuditLogListView(AdminBaseView):
#     def get(self, request):
#         logs = AuditLog.objects.all().order_by("-timestamp")
#         paginator = StandardPagination()
#         page = paginator.paginate_queryset(logs, request)
#         serializer = AuditLogSerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)

# # DASHBOARD
# class AdminDashboardView(AdminBaseView):
#     def get(self, request):
#         data = {
#             "total_staff": StaffProfile.objects.count(),
#             "active_staff": StaffProfile.objects.filter(is_active=True).count(),
#             "total_doctors": DoctorProfile.objects.count(),
#             "total_receptionists": ReceptionistProfile.objects.count(),
#             "total_lab_technicians": LabTechnicianProfile.objects.count(),
#             "total_pharmacists": PharmacistProfile.objects.count(),
#             "recent_audit_logs": list(
#                 AuditLog.objects.order_by('-timestamp')[:10].values(
#                     'log_id', 'user__username', 'action', 'module',
#                     'object_id', 'description', 'timestamp'
#                 )
#             )
#         }
#         return Response(data)
# administration/views.# administration/views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import (
    StaffProfile, DoctorProfile, ReceptionistProfile,
    LabTechnicianProfile, PharmacistProfile, AuditLog,
)
from .serializers import (
    StaffProfileSerializer, DoctorProfileSerializer,
    ReceptionistProfileSerializer, LabTechnicianProfileSerializer,
    PharmacistProfileSerializer, AuditLogSerializer,
)
from authentication.permissions import (
    IsAdminUser,
    IsDoctor,
    IsReceptionist,
    IsPharmacist,
    IsLabTechnician,
)


# ─── Pagination ──────────────────────────────────────────────────
class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# ─── Admin-only base ─────────────────────────────────────────────
class AdminOnlyView(APIView):
    """All HTTP methods require the admin role."""
    permission_classes = [IsAdminUser]


# ─── Reusable list+create ────────────────────────────────────────
class ListCreateView(AdminOnlyView):
    model = None
    serializer_class = None
    order_field = "id"

    def get_queryset(self):
        return self.model.objects.all().order_by(f"-{self.order_field}")

    def get(self, request):
        qs = self.get_queryset()
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(
            self.serializer_class(page, many=True).data
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(
                {"message": f"{self.model.__name__} created", "id": instance.pk, "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateDeleteView(AdminOnlyView):
    serializer_class = None

    def _obj(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)

    def get(self, request, pk):
        return Response(self.serializer_class(self._obj(pk)).data)

    def put(self, request, pk):
        s = self.serializer_class(self._obj(pk), data=request.data)
        if s.is_valid():
            s.save()
            return Response({"message": "Updated", "data": s.data})
        return Response({"errors": s.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        s = self.serializer_class(self._obj(pk), data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response({"message": "Updated", "data": s.data})
        return Response({"errors": s.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self._obj(pk).delete()
        return Response({"message": "Deleted"}, status=status.HTTP_204_NO_CONTENT)


# ─── Admin Dashboard ─────────────────────────────────────────────
class AdminDashboardView(AdminOnlyView):
    def get(self, request):
        return Response({
            "staff_count":        StaffProfile.objects.count(),
            "doctor_count":       DoctorProfile.objects.count(),
            "receptionist_count": ReceptionistProfile.objects.count(),
            "lab_count":          LabTechnicianProfile.objects.count(),
            "pharmacist_count":   PharmacistProfile.objects.count(),
        })


# ─── Staff ───────────────────────────────────────────────────────
class StaffListView(ListCreateView):
    model = StaffProfile
    serializer_class = StaffProfileSerializer


class StaffDetailView(RetrieveUpdateDeleteView):
    serializer_class = StaffProfileSerializer


# ─── Doctors ─────────────────────────────────────────────────────
# GET list/detail: admin + receptionist (receptionist needs doctor list for booking)
# POST/PUT/PATCH/DELETE: admin only

class DoctorListView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            # Receptionist needs the list to book appointments; doctors & admin also fine
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get(self, request):
        qs = DoctorProfile.objects.all().order_by("-id")
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(
            DoctorProfileSerializer(page, many=True).data
        )

    def post(self, request):
        s = DoctorProfileSerializer(data=request.data)
        if s.is_valid():
            instance = s.save()
            return Response({"id": instance.pk, "data": s.data}, status=status.HTTP_201_CREATED)
        return Response({"errors": s.errors}, status=status.HTTP_400_BAD_REQUEST)


class DoctorDetailView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def _obj(self, pk):
        return get_object_or_404(DoctorProfile, pk=pk)

    def get(self, request, pk):
        return Response(DoctorProfileSerializer(self._obj(pk)).data)

    def put(self, request, pk):
        s = DoctorProfileSerializer(self._obj(pk), data=request.data)
        if s.is_valid():
            s.save(); return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        s = DoctorProfileSerializer(self._obj(pk), data=request.data, partial=True)
        if s.is_valid():
            s.save(); return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self._obj(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─── Receptionists (admin only) ──────────────────────────────────
class ReceptionistListView(ListCreateView):
    model = ReceptionistProfile
    serializer_class = ReceptionistProfileSerializer


class ReceptionistDetailView(RetrieveUpdateDeleteView):
    serializer_class = ReceptionistProfileSerializer


# ─── Lab Technicians (admin only) ────────────────────────────────
class LabTechnicianListView(ListCreateView):
    model = LabTechnicianProfile
    serializer_class = LabTechnicianProfileSerializer


class LabTechnicianDetailView(RetrieveUpdateDeleteView):
    serializer_class = LabTechnicianProfileSerializer


# ─── Pharmacists (admin only) ────────────────────────────────────
class PharmacistListView(ListCreateView):
    model = PharmacistProfile
    serializer_class = PharmacistProfileSerializer


class PharmacistDetailView(RetrieveUpdateDeleteView):
    serializer_class = PharmacistProfileSerializer


# ─── Audit Log (admin only) ──────────────────────────────────────
class AuditLogListView(AdminOnlyView):
    def get(self, request):
        qs = AuditLog.objects.all().order_by("-id")
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(
            AuditLogSerializer(page, many=True).data
        )


# ─── Self-profile endpoints (each role reads only their own) ─────
class DoctorSelfView(APIView):
    permission_classes = [IsDoctor]

    def get(self, request):
        profile = get_object_or_404(DoctorProfile, staff_profile__user=request.user)
        return Response(DoctorProfileSerializer(profile).data)


class ReceptionistSelfView(APIView):
    permission_classes = [IsReceptionist]

    def get(self, request):
        profile = get_object_or_404(ReceptionistProfile, staff_profile__user=request.user)
        return Response(ReceptionistProfileSerializer(profile).data)


class PharmacistSelfView(APIView):
    permission_classes = [IsPharmacist]

    def get(self, request):
        profile = get_object_or_404(PharmacistProfile, staff_profile__user=request.user)
        return Response(PharmacistProfileSerializer(profile).data)


class LabTechnicianSelfView(APIView):
    permission_classes = [IsLabTechnician]

    def get(self, request):
        profile = get_object_or_404(LabTechnicianProfile, staff_profile__user=request.user)
        return Response(LabTechnicianProfileSerializer(profile).data)