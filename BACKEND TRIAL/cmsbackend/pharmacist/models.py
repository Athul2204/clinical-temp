from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from administration.models import PharmacistProfile
from doctor.models import Prescription


# =========================
# MEDICINE MASTER
# =========================

class Medicine(models.Model):
    medicine_name = models.CharField(max_length=150, unique=True)
    manufacturer = models.CharField(max_length=150)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.selling_price <= 0:
            raise ValidationError("Selling price must be positive")

    def __str__(self):
        return self.medicine_name


# =========================
# MEDICINE BATCH
# =========================

class MedicineBatch(models.Model):

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Expired", "Expired"),
        ("Returned", "Returned"),
    ]

    batch_code = models.CharField(max_length=20, unique=True, editable=False)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    batch_number = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Available")

    def clean(self):

        if self.quantity < 0:
            raise ValidationError("Quantity cannot be negative")

        if self.expiry_date < timezone.now().date():
            self.status = "Expired"

    def save(self, *args, **kwargs):

        if not self.batch_code:
            last = MedicineBatch.objects.order_by("-id").first()
            if last:
                last_number = int(last.batch_code.split("-")[1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.batch_code = f"MB-{str(new_number).zfill(3)}"

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.batch_code


# =========================
# STOCK LOG
# =========================

class MedicineStockLog(models.Model):

    ACTION_CHOICES = [
        ("ADD", "Add"),
        ("DISPENSE", "Dispense"),
        ("EXPIRE", "Expire"),
        ("RETURN", "Return"),
    ]

    batch = models.ForeignKey(MedicineBatch, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


# =========================
# DISPENSE
# =========================

class Dispense(models.Model):

    dispense_code = models.CharField(max_length=20, unique=True, editable=False)
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name="dispenses"
    )
    pharmacist = models.ForeignKey(
        PharmacistProfile,
        on_delete=models.PROTECT
    )
    dispensed_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.prescription.status != "Sent":
            raise ValidationError("Prescription must be Sent before dispensing")

    def save(self, *args, **kwargs):

        if not self.dispense_code:
            last = Dispense.objects.order_by("-id").first()
            if last:
                last_number = int(last.dispense_code.split("-")[1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.dispense_code = f"DP-{str(new_number).zfill(3)}"

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.dispense_code


# =========================
# DISPENSE ITEM
# =========================

class DispenseItem(models.Model):

    dispense = models.ForeignKey(
        Dispense,
        on_delete=models.CASCADE,
        related_name="items"
    )
    batch = models.ForeignKey(
        MedicineBatch,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField()

    def clean(self):

        if self.batch.status != "Available":
            raise ValidationError("Cannot dispense expired or returned batch")

        if self.quantity <= 0:
            raise ValidationError("Quantity must be positive")

        if self.quantity > self.batch.quantity:
            raise ValidationError("Insufficient stock in this batch")

    def save(self, *args, **kwargs):

        self.full_clean()

        # Deduct stock
        self.batch.quantity -= self.quantity

        if self.batch.quantity == 0:
            self.batch.status = "Expired"

        self.batch.save()

        # Log stock change
        MedicineStockLog.objects.create(
            batch=self.batch,
            action="DISPENSE",
            quantity=self.quantity
        )

        super().save(*args, **kwargs)


# =========================
# MEDICINE BILL
# =========================

class MedicineBill(models.Model):

    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
    ]

    bill_code = models.CharField(max_length=20, unique=True, editable=False)
    dispense = models.OneToOneField(
        Dispense,
        on_delete=models.CASCADE,
        related_name="medicine_bill"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        total = sum(
            item.quantity * item.batch.medicine.selling_price
            for item in self.dispense.items.all()
        )

        if self.discount < 0:
            raise ValidationError("Discount cannot be negative")

        if self.discount > total:
            raise ValidationError("Discount cannot exceed total")

        return total - self.discount

    def save(self, *args, **kwargs):

        if not self.bill_code:
            last = MedicineBill.objects.order_by("-id").first()
            if last:
                last_number = int(last.bill_code.split("-")[1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.bill_code = f"BILL-{str(new_number).zfill(3)}"

        self.total_amount = self.calculate_total()

        super().save(*args, **kwargs)

        # Mark prescription as dispensed
        self.dispense.prescription.status = "Dispensed"
        self.dispense.prescription.save()

    def __str__(self):
        return self.bill_code