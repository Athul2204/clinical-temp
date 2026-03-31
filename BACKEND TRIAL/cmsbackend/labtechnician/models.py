from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator


# ------------------------------
# Lab Test Table
# ------------------------------
class LabTest(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    normal_range = models.CharField(max_length=100, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.test_name


# ------------------------------
# Lab Order Table
# ------------------------------
class LabOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    
    lab_request = models.ForeignKey(
        "doctor.LabTestRequest",
        on_delete=models.CASCADE,
        related_name="lab_orders"
    )
    
    patient = models.ForeignKey(
        "reception.Patient",
        on_delete=models.CASCADE
    )
    
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed")
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def clean(self):
        expected_patient = self.lab_request.consultation.appointment.patient
        if self.patient_id != expected_patient.pk:
            raise ValidationError({
                "patient": "Patient must match the patient in the linked lab request."
            })
        
        # Prevent duplicate orders for same request
        if LabOrder.objects.filter(lab_request=self.lab_request).exclude(pk=self.pk).exists():
            raise ValidationError("Lab order already exists for this request")

    def save(self, *args, **kwargs):
        self.full_clean()

        # ✅ AUTO GENERATE ORDER NUMBER
        if not self.order_number:
            last = LabOrder.objects.order_by("-order_id").first()
            new_number = 1
            if last:
                try:
                    last_number = int(last.order_number.split("-")[1])
                    new_number = last_number + 1
                except:
                    pass
            self.order_number = f"LAB-{str(new_number).zfill(3)}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


# ------------------------------
# Lab Order Item Table
# ------------------------------
class LabOrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)

    lab_order = models.ForeignKey(
        LabOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )

    lab_test = models.ForeignKey(
        LabTest,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("lab_order", "lab_test")

    def clean(self):
        duplicate_exists = LabOrderItem.objects.filter(
            lab_order=self.lab_order,
            lab_test=self.lab_test,
        ).exclude(pk=self.pk).exists()

        if duplicate_exists:
            raise ValidationError({
                "lab_test": "This test is already added for the selected order."
            })

    def __str__(self):
        return f"{self.lab_test.test_name} in {self.lab_order.order_number}"


# ------------------------------
# Lab Result Table
# ------------------------------
class LabResult(models.Model):
    result_id = models.AutoField(primary_key=True)

    lab_order_item = models.OneToOneField(
        LabOrderItem,
        on_delete=models.CASCADE
    )

    result_value = models.CharField(max_length=200)
    remarks = models.TextField(blank=True, null=True)

    is_critical = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def clean(self):
        if not str(self.result_value).strip():
            raise ValidationError({"result_value": "Result value cannot be empty."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        lab_order = self.lab_order_item.lab_order

        total_tests = lab_order.items.count()

        completed_results = LabResult.objects.filter(
            lab_order_item__lab_order=lab_order
        ).count()

        # ✅ AUTO COMPLETE FLOW
        if total_tests == completed_results:

            # 1️⃣ LabOrder → Completed
            lab_order.status = "Completed"
            lab_order.save(update_fields=["status"])

            # 2️⃣ LabTestRequest → Completed
            lab_request = lab_order.lab_request
            lab_request.status = "Completed"
            lab_request.completed_at = timezone.now()
            lab_request.save(update_fields=["status", "completed_at"])

    def __str__(self):
        return f"Result {self.result_id} - {self.lab_order_item.lab_test.test_name}"


# ------------------------------
# Lab Bill Table
# ------------------------------
class LabBill(models.Model):
    lab_bill_id = models.AutoField(primary_key=True)

    bill_number = models.CharField(max_length=20, unique=True, blank=True)

    lab_order = models.OneToOneField(
        LabOrder,
        on_delete=models.CASCADE
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    final_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    payment_status_choices = [("Pending", "Pending"), ("Paid", "Paid")]
    payment_status = models.CharField(max_length=20, choices=payment_status_choices, default="Pending")

    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def clean(self):
        if self.total_amount < 0:
            raise ValidationError({"total_amount": "Total amount cannot be negative."})

        if self.discount < 0:
            raise ValidationError({"discount": "Discount cannot be negative."})

        if self.discount > self.total_amount:
            raise ValidationError({"discount": "Discount cannot exceed total amount."})

    def save(self, *args, **kwargs):
        # ✅ AUTO BILL NUMBER — must happen BEFORE full_clean()
        if not self.bill_number:
            last = LabBill.objects.order_by("-lab_bill_id").first()
            new_number = 1
            if last:
                try:
                    last_number = int(last.bill_number.split("-")[1])
                    new_number = last_number + 1
                except:
                    pass
            self.bill_number = f"BILL-{str(new_number).zfill(3)}"

        self.final_amount = self.total_amount - self.discount

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.bill_number
    


# ------------------------------
# Lab Equipment Table
# ------------------------------
class LabEquipment(models.Model):
    equipment_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=200)

    purchase_date = models.DateField()
    last_service_date = models.DateField(blank=True, null=True)

    status_choices = [
        ("Available", "Available"),
        ("Under Maintenance", "Under Maintenance"),
        ("Out of Service", "Out of Service")
    ]

    status = models.CharField(max_length=50, choices=status_choices, default="Available")

    def clean(self):
        if self.last_service_date and self.last_service_date < self.purchase_date:
            raise ValidationError({
                "last_service_date": "Last service date cannot be before purchase date."
            })

    def __str__(self):
        return self.name


# ------------------------------
# Lab Maintenance Table
# ------------------------------
class LabMaintenance(models.Model):
    maintenance_id = models.AutoField(primary_key=True)

    equipment = models.ForeignKey(
        LabEquipment,
        on_delete=models.CASCADE,
        related_name="maintenance_records"
    )

    service_date = models.DateField()

    technician_name = models.CharField(max_length=100)

    remarks = models.TextField(blank=True, null=True)

    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def clean(self):
        if self.service_date < self.equipment.purchase_date:
            raise ValidationError({
                "service_date": "Service date cannot be before equipment purchase date."
            })

    def __str__(self):
        return f"Maintenance {self.maintenance_id} - {self.equipment.name}"