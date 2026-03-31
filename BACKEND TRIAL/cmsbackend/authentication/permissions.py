from rest_framework.permissions import BasePermission

class IsPharmacist(BasePermission):
    def has_permission(self, request, view):
        # Check Django group (if used) OR StaffProfile role
        if request.user.groups.filter(name="Pharmacist").exists():
            return True
        staff_profile = getattr(request.user, "staff_profile", None)
        return staff_profile is not None and staff_profile.role == "Pharmacist"

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="Doctor").exists():
            return True
        staff_profile = getattr(request.user, "staff_profile", None)
        return staff_profile is not None and staff_profile.role == "Doctor"

class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="Receptionist").exists():
            return True
        staff_profile = getattr(request.user, "staff_profile", None)
        return staff_profile is not None and staff_profile.role == "Receptionist"

class IsLabTechnician(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="LabTechnician").exists():
            return True
        staff_profile = getattr(request.user, "staff_profile", None)
        return staff_profile is not None and staff_profile.role == "Lab Technician"

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff