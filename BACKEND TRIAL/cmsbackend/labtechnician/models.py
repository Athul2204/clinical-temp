from django.db import models
from administration.models import LabTechnicianProfile, DoctorProfile
from reception.models import Appointment


class LabTest(models.Model):
    test_name = models.CharField(max_length=150, unique=True)
    category = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    normal_range = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class LabOrder(models.Model):
    lab_order_code = models.CharField(max_length=20, unique=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.PROTECT)
    status = models.CharField(max_length=30, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)


class LabOrderItem(models.Model):
    lab_order = models.ForeignKey(LabOrder, on_delete=models.CASCADE)
    lab_test = models.ForeignKey(LabTest, on_delete=models.PROTECT)


class LabResult(models.Model):
    lab_order = models.OneToOneField(LabOrder, on_delete=models.CASCADE)
    technician = models.ForeignKey(LabTechnicianProfile, on_delete=models.PROTECT)
    result_data = models.JSONField()
    is_critical = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)


class LabBill(models.Model):
    bill_code = models.CharField(max_length=20, unique=True)
    lab_order = models.OneToOneField(LabOrder, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)


class LabEquipment(models.Model):
    equipment_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    status = models.CharField(max_length=30, default="Available")


class LabMaintenance(models.Model):
    equipment = models.ForeignKey(LabEquipment, on_delete=models.CASCADE)
    technician = models.ForeignKey(LabTechnicianProfile, on_delete=models.PROTECT)
    issue = models.TextField()
    action_taken = models.TextField()
    maintenance_date = models.DateTimeField(auto_now_add=True)