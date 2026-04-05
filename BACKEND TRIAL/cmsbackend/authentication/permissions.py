# authentication/permissions.py
from rest_framework.permissions import BasePermission


def _get_role(user):
    """
    Returns the normalised lowercase role string for any user.
    Superusers / is_staff with no StaffProfile -> 'admin'.
    """
    if not user or not user.is_authenticated:
        return None
    staff_profile = getattr(user, "staff_profile", None)
    if staff_profile:
        return staff_profile.role.lower().replace(" ", "")
    if user.is_staff:
        return "admin"
    return None


class IsAdminUser(BasePermission):
    message = "Access denied. Admin role required."

    def has_permission(self, request, view):
        role = _get_role(request.user)
        return role == "admin"


class IsDoctor(BasePermission):
    message = "Access denied. Doctor role required."

    def has_permission(self, request, view):
        return _get_role(request.user) == "doctor"


class IsReceptionist(BasePermission):
    message = "Access denied. Receptionist role required."

    def has_permission(self, request, view):
        return _get_role(request.user) == "receptionist"


class IsPharmacist(BasePermission):
    message = "Access denied. Pharmacist role required."

    def has_permission(self, request, view):
        return _get_role(request.user) == "pharmacist"


class IsLabTechnician(BasePermission):
    message = "Access denied. Lab Technician role required."

    def has_permission(self, request, view):
        return _get_role(request.user) == "labtechnician"


class IsAdminOrDoctor(BasePermission):
    """Admin or Doctor — used for endpoints both roles need to read."""
    message = "Access denied. Admin or Doctor role required."

    def has_permission(self, request, view):
        return _get_role(request.user) in ("admin", "doctor")


class IsAdminOrReceptionist(BasePermission):
    """Admin or Receptionist."""
    message = "Access denied. Admin or Receptionist role required."

    def has_permission(self, request, view):
        return _get_role(request.user) in ("admin", "receptionist")