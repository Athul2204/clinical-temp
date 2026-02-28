from django.db import models
from administration.models import LabTechnicianProfile, DoctorProfile
from reception.models import Appointment


# =========================
# LAB TEST MASTER
# =========================

class LabTest(models.Model):
    test_name = models.CharField(max_length=150, unique=True)
    category = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    normal_range = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.test_name


# =========================
# LAB ORDER
# =========================

class LabOrder(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    lab_order_code = models.CharField(max_length=20, unique=True)
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name="lab_orders"
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        related_name="lab_orders"
    )
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lab_order_code


# =========================
# LAB ORDER ITEMS
# =========================

class LabOrderItem(models.Model):
    lab_order = models.ForeignKey(
        LabOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )
    lab_test = models.ForeignKey(
        LabTest,
        on_delete=models.PROTECT,
        related_name="order_items"
    )

    def __str__(self):
        return f"{self.lab_order} - {self.lab_test}"


# =========================
# LAB RESULT
# =========================

class LabResult(models.Model):
    lab_order = models.OneToOneField(
        LabOrder,
        on_delete=models.CASCADE,
        related_name="result"
    )
    lab_technician = models.ForeignKey(
        LabTechnicianProfile,
        on_delete=models.PROTECT,
        related_name="results"
    )
    result_data = models.JSONField()
    remarks = models.TextField(blank=True)
    is_critical = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result - {self.lab_order}"


# =========================
# LAB BILL (LAB TECHNICIAN)
# =========================

class LabBill(models.Model):
    bill_code = models.CharField(max_length=20, unique=True)
    lab_order = models.OneToOneField(
        LabOrder,
        on_delete=models.CASCADE,
        related_name="lab_bill"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=30)
    payment_mode = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bill_code