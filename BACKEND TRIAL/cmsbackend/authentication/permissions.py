from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsDoctor(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Doctor").exists()


class IsReceptionist(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Receptionist").exists()


class IsPharmacist(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Pharmacist").exists()


class IsLabTechnician(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="LabTechnician").exists()