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


import random


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def generate_otp():
    return random.randint(100000, 999999)