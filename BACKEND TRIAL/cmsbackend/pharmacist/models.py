from django.db import models
from administration.models import PharmacistProfile
from doctor.models import Prescription


class Medicine(models.Model):
    medicine_name = models.CharField(max_length=150, unique=True)
    manufacturer = models.CharField(max_length=150)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)


class MedicineBatch(models.Model):
    batch_code = models.CharField(max_length=20, unique=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    batch_number = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=30)


class Dispense(models.Model):
    dispense_code = models.CharField(max_length=20, unique=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    pharmacist = models.ForeignKey(PharmacistProfile, on_delete=models.PROTECT)
    dispensed_at = models.DateTimeField(auto_now_add=True)


class DispenseItem(models.Model):
    dispense = models.ForeignKey(Dispense, on_delete=models.CASCADE)
    batch = models.ForeignKey(MedicineBatch, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()


class MedicineBill(models.Model):
    bill_code = models.CharField(max_length=20, unique=True)
    dispense = models.OneToOneField(Dispense, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)


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
# from django.db import models

# # Create your models here.
# from django.db import models
# from administration.models import PharmacistProfile
# from doctor.models import Prescription


# # =========================
# # MEDICINE MASTER
# # =========================

# class Medicine(models.Model):
#     medicine_name = models.CharField(max_length=150, unique=True)
#     manufacturer = models.CharField(max_length=150, blank=True)
#     selling_price = models.DecimalField(max_digits=10, decimal_places=2)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.medicine_name


# # =========================
# # MEDICINE BATCH (INVENTORY)
# # =========================

# class MedicineBatch(models.Model):
#     batch_code = models.CharField(max_length=20, unique=True)
#     medicine = models.ForeignKey(
#         Medicine,
#         on_delete=models.PROTECT,
#         related_name="batches"
#     )
#     batch_number = models.CharField(max_length=100)
#     quantity = models.PositiveIntegerField()
#     expiry_date = models.DateField()
#     status = models.CharField(max_length=30)

#     def __str__(self):
#         return f"{self.medicine} - {self.batch_code}"


# # =========================
# # DISPENSE
# # =========================

# class Dispense(models.Model):
#     dispense_code = models.CharField(max_length=20, unique=True)
#     prescription = models.ForeignKey(
#         Prescription,
#         on_delete=models.CASCADE,
#         related_name="dispenses"
#     )
#     pharmacist = models.ForeignKey(
#         PharmacistProfile,
#         on_delete=models.PROTECT,
#         related_name="dispenses"
#     )
#     dispensed_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.dispense_code


# # =========================
# # DISPENSE ITEMS
# # =========================

# class DispenseItem(models.Model):
#     dispense = models.ForeignKey(
#         Dispense,
#         on_delete=models.CASCADE,
#         related_name="items"
#     )
#     batch = models.ForeignKey(
#         MedicineBatch,
#         on_delete=models.PROTECT,
#         related_name="dispense_items"
#     )
#     quantity = models.PositiveIntegerField()

#     def __str__(self):
#         return f"{self.batch} - {self.quantity}"


# # =========================
# # MEDICINE BILL (PHARMACIST)
# # =========================

# class MedicineBill(models.Model):
#     bill_code = models.CharField(max_length=20, unique=True)
#     dispense = models.OneToOneField(
#         Dispense,
#         on_delete=models.CASCADE,
#         related_name="medicine_bill"
#     )
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     discount = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         default=0
#     )
#     payment_status = models.CharField(max_length=30)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.bill_code