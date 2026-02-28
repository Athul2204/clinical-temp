from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from administration.models import LabTechnicianProfile, DoctorProfile
from reception.models import Appointment


# =========================
# LAB TEST MASTER
# =========================

class LabTest(models.Model):
    test_name = models.CharField(max_length=150, unique=True)
    category = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    normal_range = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.price <= 0:
            raise ValidationError("Price must be positive")

    def __str__(self):
        return self.test_name


# =========================
# LAB ORDER
# =========================

class LabOrder(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
    ]

    lab_order_code = models.CharField(max_length=20, unique=True, editable=False)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.PROTECT)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.lab_order_code:
            last = LabOrder.objects.order_by("-id").first()
            if last:
                last_number = int(last.lab_order_code.split("-")[1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.lab_order_code = f"LAB-{str(new_number).zfill(3)}"

        super().save(*args, **kwargs)

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
    lab_test = models.ForeignKey(LabTest, on_delete=models.PROTECT)


# =========================
# LAB RESULT
# =========================

class LabResult(models.Model):

    lab_order = models.OneToOneField(LabOrder, on_delete=models.CASCADE)
    technician = models.ForeignKey(LabTechnicianProfile, on_delete=models.PROTECT)
    result_data = models.JSONField()
    is_critical = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    def clean(self):

        # Prevent duplicate result
        if LabResult.objects.filter(lab_order=self.lab_order).exclude(id=self.id).exists():
            raise ValidationError("Result already recorded for this lab order")

    def evaluate_critical(self):
        """
        Example simple rule:
        If any numeric value in result_data is abnormal,
        flag as critical manually by technician later.
        (Can extend with AI/range logic)
        """
        # Placeholder logic
        if "critical" in str(self.result_data).lower():
            self.is_critical = True

    def save(self, *args, **kwargs):

        self.evaluate_critical()
        self.full_clean()
        super().save(*args, **kwargs)

        # Auto update lab order status
        self.lab_order.status = "Completed"
        self.lab_order.save()

    def __str__(self):
        return f"Result - {self.lab_order.lab_order_code}"


# =========================
# LAB BILL
# =========================

class LabBill(models.Model):

    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
    ]

    bill_code = models.CharField(max_length=20, unique=True, editable=False)
    lab_order = models.OneToOneField(LabOrder, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        total = sum(item.lab_test.price for item in self.lab_order.items.all())
        if self.discount < 0:
            raise ValidationError("Discount cannot be negative")
        if self.discount > total:
            raise ValidationError("Discount cannot exceed total")
        return total - self.discount

    def save(self, *args, **kwargs):

        if not self.bill_code:
            last = LabBill.objects.order_by("-id").first()
            if last:
                last_number = int(last.bill_code.split("-")[1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.bill_code = f"LB-{str(new_number).zfill(3)}"

        self.total_amount = self.calculate_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.bill_code


# =========================
# LAB EQUIPMENT
# =========================

class LabEquipment(models.Model):

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Under Maintenance", "Under Maintenance"),
    ]

    equipment_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Available")

    def __str__(self):
        return self.name


# =========================
# LAB MAINTENANCE
# =========================

class LabMaintenance(models.Model):
    equipment = models.ForeignKey(LabEquipment, on_delete=models.CASCADE)
    technician = models.ForeignKey(LabTechnicianProfile, on_delete=models.PROTECT)
    issue = models.TextField()
    action_taken = models.TextField()
    maintenance_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        # Mark equipment under maintenance
        self.equipment.status = "Under Maintenance"
        self.equipment.save()

        super().save(*args, **kwargs)