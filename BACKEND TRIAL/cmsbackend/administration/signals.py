from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import (
    StaffProfile,
    DoctorProfile,
    ReceptionistProfile,
    LabTechnicianProfile,
    PharmacistProfile,
    AuditLog
)


# ------------------------------
# Helper Function
# ------------------------------
def create_log(instance, action, module_name):
    AuditLog.objects.create(
        user=getattr(instance, 'user', None),
        module=module_name,
        action=action,
        object_id=instance.pk,
        description=f"{module_name} {action} with ID {instance.pk}"
    )


# ------------------------------
# Staff Profile Signals
# ------------------------------
@receiver(post_save, sender=StaffProfile)
def log_staff_save(sender, instance, created, **kwargs):
    if created:
        create_log(instance, "CREATED", "Administration")
    else:
        create_log(instance, "UPDATED", "Administration")


@receiver(post_delete, sender=StaffProfile)
def log_staff_delete(sender, instance, **kwargs):
    create_log(instance, "DELETED", "Administration")


# ------------------------------
# Doctor Signals
# ------------------------------
@receiver(post_save, sender=DoctorProfile)
def log_doctor_save(sender, instance, created, **kwargs):
    action = "CREATED" if created else "UPDATED"
    create_log(instance.staff, action, "Doctor")


@receiver(post_delete, sender=DoctorProfile)
def log_doctor_delete(sender, instance, **kwargs):
    create_log(instance.staff, "DELETED", "Doctor")


# ------------------------------
# Receptionist Signals
# ------------------------------
@receiver(post_save, sender=ReceptionistProfile)
def log_reception_save(sender, instance, created, **kwargs):
    action = "CREATED" if created else "UPDATED"
    create_log(instance.staff, action, "Reception")


@receiver(post_delete, sender=ReceptionistProfile)
def log_reception_delete(sender, instance, **kwargs):
    create_log(instance.staff, "DELETED", "Reception")


# ------------------------------
# Lab Technician Signals
# ------------------------------
@receiver(post_save, sender=LabTechnicianProfile)
def log_labtech_save(sender, instance, created, **kwargs):
    action = "CREATED" if created else "UPDATED"
    create_log(instance.staff, action, "Laboratory")


@receiver(post_delete, sender=LabTechnicianProfile)
def log_labtech_delete(sender, instance, **kwargs):
    create_log(instance.staff, "DELETED", "Laboratory")


# ------------------------------
# Pharmacist Signals
# ------------------------------
@receiver(post_save, sender=PharmacistProfile)
def log_pharmacist_save(sender, instance, created, **kwargs):
    action = "CREATED" if created else "UPDATED"
    create_log(instance.staff, action, "Pharmacy")


@receiver(post_delete, sender=PharmacistProfile)
def log_pharmacist_delete(sender, instance, **kwargs):
    create_log(instance.staff, "DELETED", "Pharmacy")