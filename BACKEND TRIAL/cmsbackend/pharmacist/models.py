
# from django.db import models
# from django.core.exceptions import ValidationError
# from django.utils import timezone
# from django.core.validators import MinValueValidator

# # ------------------------------
# # Medicine Table
# # ------------------------------
# class Medicine(models.Model):
#     medicine_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=200,unique=True)
#     description = models.TextField(blank=True, null=True)
#     unit = models.CharField(max_length=50, blank=True, null=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
#     def clean(self):
#         #  ADDED: price must be greater than 0 (not just >= 0)
#         if self.price is not None and self.price <= 0:
#             raise ValidationError({'price': 'Medicine price must be greater than zero.'})

#         #  ADDED: name should not be blank/whitespace
#         if self.name and not self.name.strip():
#             raise ValidationError({'name': 'Medicine name cannot be blank or whitespace.'})
#     def save(self, *args, **kwargs):
#         self.full_clean()        # ← this triggers clean() before saving
#         super().save(*args, **kwargs)
#     def __str__(self):
#         return self.name


# # ------------------------------
# # Medicine Batch Table
# # ------------------------------
# class MedicineBatch(models.Model):
#     batch_id = models.AutoField(primary_key=True)
#     medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='batches')
#     batch_number = models.CharField(max_length=50,unique=True,blank=True)
#     quantity = models.PositiveIntegerField()
#     expiry_date = models.DateField()
#     created_at = models.DateTimeField(default=timezone.now, editable=False)

#     # class Meta:
#     #     unique_together = ('medicine', 'batch_number')
#     def clean(self):
#         #  ADDED: expiry date must be in the future
#         if self.expiry_date and self.expiry_date < timezone.now().date():
#             raise ValidationError({'expiry_date': 'Expiry date must be a future date.'})

#         #  ADDED: quantity must be at least 1
#         if self.quantity is not None and self.quantity < 1:
#             raise ValidationError({'quantity': 'Batch quantity must be at least 1.'})
#     # def save(self, *args, **kwargs):
#     #     if not self.batch_number:
#     #         last_batch = MedicineBatch.objects.filter(
#     #             medicine=self.medicine
#     #         ).order_by('-batch_id').first()

#     #         if last_batch:
#     #             last_number = int(last_batch.batch_number[1:])  # remove 'B'
#     #             next_number = last_number + 1
#     #         else:
#     #             next_number = 1

#     #         self.batch_number = f"B{str(next_number).zfill(3)}"  # B001, B002

#     #     self.full_clean()        # ← this triggers clean() before saving
#     #     super().save(*args, **kwargs)
#     def save(self, *args, **kwargs):
#         if not self.batch_number:
#             # Global last batch (not per-medicine, since batch_number is globally unique)
#             last_batch = MedicineBatch.objects.order_by('-batch_id').first()
#             next_number = (int(last_batch.batch_number[1:]) + 1) if last_batch else 1

#             # Loop until unique (avoids 500 error from full_clean)
#             candidate = f"B{str(next_number).zfill(3)}"
#             while MedicineBatch.objects.filter(batch_number=candidate).exists():
#                 next_number += 1
#                 candidate = f"B{str(next_number).zfill(3)}"

#             self.batch_number = candidate

#         self.full_clean()
#         super().save(*args, **kwargs)
#     def __str__(self):
#         return f"{self.medicine.name} - {self.batch_number}"


# # ------------------------------
# # Medicine Stock Log Table
# # ------------------------------
# class MedicineStockLog(models.Model):
#     log_id = models.AutoField(primary_key=True)
#     batch = models.ForeignKey(MedicineBatch, on_delete=models.CASCADE, related_name='stock_logs')
#     change_type_choices = [('ADD', 'Added'), ('DISPENSE', 'Dispensed'), ('EXPIRED', 'Expired')]
#     change_type = models.CharField(max_length=20, choices=change_type_choices)
#     quantity_changed = models.IntegerField()
#     created_at = models.DateTimeField(default=timezone.now, editable=False)
#     remarks = models.TextField(blank=True, null=True)

#     def clean(self):
#         #  ADDED: quantity_changed must not be zero
#         if self.quantity_changed == 0:
#             raise ValidationError({'quantity_changed': 'Quantity changed cannot be zero.'})

#         #  ADDED: DISPENSE and EXPIRED should be negative, ADD should be positive
#         if self.change_type in ('DISPENSE', 'EXPIRED') and self.quantity_changed > 0:
#             raise ValidationError({
#                 'quantity_changed': f'{self.change_type} must have a negative quantity (stock is going out).'
#             })
#         if self.change_type == 'ADD' and self.quantity_changed < 0:
#             raise ValidationError({
#                 'quantity_changed': 'ADD must have a positive quantity (stock is coming in).'
#             })

#         #  ADDED: cannot dispense more than available batch quantity
#         if self.change_type == 'DISPENSE' and self.batch_id:
#             available = self.batch.quantity
#             if abs(self.quantity_changed) > available:
#                 raise ValidationError({
#                     'quantity_changed': f'Cannot dispense {abs(self.quantity_changed)} units. Only {available} available in this batch.'
#                 })
#     def save(self, *args, **kwargs):
#         self.full_clean()        # ← this triggers clean() before saving
#         super().save(*args, **kwargs)
# # ------------------------------
# # Dispense Table
# # ------------------------------
# class Dispense(models.Model):
#     dispense_id = models.AutoField(primary_key=True)
#     prescription = models.ForeignKey("doctor.Prescription", on_delete=models.CASCADE, related_name='dispenses')
#     patient = models.ForeignKey("reception.Patient", on_delete=models.CASCADE)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     dispense_date = models.DateTimeField(default=timezone.now, editable=False)
#     status_choices = [('Pending', 'Pending'), ('Completed', 'Completed')]
#     status = models.CharField(max_length=20, choices=status_choices, default='Pending')
    
#     def clean(self):
#         #  ADDED: total_amount must be greater than 0
#         if self.total_amount is not None and self.total_amount <= 0:
#             raise ValidationError({'total_amount': 'Dispense total amount must be greater than zero.'})
#     def save(self, *args, **kwargs):
#         #self.full_clean()        # ← this triggers clean() before saving
#         super().save(*args, **kwargs)
#     def __str__(self):
#         return f"Dispense {self.dispense_id} - {self.patient.first_name}"


# # ------------------------------
# # Dispense Item Table
# # ------------------------------
# class DispenseItem(models.Model):
#     dispense_item_id = models.AutoField(primary_key=True)
#     dispense = models.ForeignKey(Dispense, on_delete=models.CASCADE, related_name='items')
#     batch = models.ForeignKey(MedicineBatch, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
#     remarks=models.TextField(blank=True,null=True)
#     def clean(self):
#         #  ADDED: quantity must be at least 1
#         if self.quantity is not None and self.quantity < 1:
#             raise ValidationError({'quantity': 'Dispense item quantity must be at least 1.'})

#         #  ADDED: cannot dispense an expired batch
#         if self.batch_id and self.batch.expiry_date < timezone.now().date():
#             raise ValidationError({'batch': f'Batch {self.batch.batch_number} has expired and cannot be dispensed.'})

#         #  ADDED: quantity requested must not exceed available stock
#         # if self.batch_id and self.quantity and self.quantity > self.batch.quantity:
#         #     raise ValidationError({
#         #         'quantity': f'Requested {self.quantity} exceeds available stock of {self.batch.quantity}.'
#         #     })

#         #  ADDED: price must match the medicine's listed price
#         if self.batch_id and self.price and self.price != self.batch.medicine.price:
#             raise ValidationError({
#                 'price': f'Price must match the medicine price of {self.batch.medicine.price}.'
#             })
#     def save(self, *args, **kwargs):
#         self.price = self.batch.medicine.price
#         self.full_clean()        # ← this triggers clean() before saving
#         super().save(*args, **kwargs)
#         #self.dispense.update_total()
#     def __str__(self):
#         return f"{self.batch.medicine.name} x {self.quantity}"


# # ------------------------------
# # Medicine Bill Table
# # ------------------------------
# class MedicineBill(models.Model):
#     bill_id = models.AutoField(primary_key=True)
#     dispense = models.OneToOneField(Dispense, on_delete=models.CASCADE)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
#     final_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
#     payment_status_choices = [('Pending', 'Pending'), ('Paid', 'Paid')]
#     payment_status = models.CharField(max_length=20, choices=payment_status_choices, default='Pending')
#     created_at = models.DateTimeField(default=timezone.now, editable=False)

#     # def save(self, *args, **kwargs):
#     #     self.final_amount = max(self.total_amount - self.discount, 0)
#     #     super().save(*args, **kwargs)

#     # def clean(self):
#     #     if self.total_amount < 0:
#     #         raise ValidationError("Total amount cannot be negative")
#     #     if self.final_amount < 0:
#     #         raise ValidationError("Final amount cannot be negative")
#     def clean(self):
#         #  FIXED: your original clean() was incomplete — moved checks here properly
#         if self.total_amount is not None and self.total_amount <= 0:
#             raise ValidationError({'total_amount': 'Total amount must be greater than zero.'})

#         #  ADDED: discount cannot exceed total amount
#         if self.discount is not None and self.total_amount is not None:
#             if self.discount > self.total_amount:
#                 raise ValidationError({'discount': 'Discount cannot be greater than the total amount.'})

#         #  ADDED: bill total must match the linked dispense total
#         if self.dispense_id and self.total_amount != self.dispense.total_amount:
#             raise ValidationError({
#                 'total_amount': 'Bill total amount must match the linked dispense total amount.'
#             })

#     def save(self, *args, **kwargs):
#         self.full_clean()  #  ADDED: always run clean() before saving
#         self.final_amount = max(self.total_amount - self.discount, 0)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Bill {self.bill_id} - {self.dispense.patient.first_name}"

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator


# ------------------------------
# Medicine
# ------------------------------
class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def clean(self):
        if self.price <= 0:
            raise ValidationError({'price': 'Must be greater than zero.'})

        if not self.name.strip():
            raise ValidationError({'name': 'Cannot be blank.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ------------------------------
# Medicine Batch
# ------------------------------
class MedicineBatch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='batches')
    batch_number = models.CharField(max_length=50, unique=True, blank=True)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        if self.expiry_date < timezone.now().date():
            raise ValidationError({'expiry_date': 'Must be future date.'})

        if self.quantity < 1:
            raise ValidationError({'quantity': 'Minimum 1 required.'})

    def save(self, *args, **kwargs):
        if not self.batch_number:
            last = MedicineBatch.objects.order_by('-batch_id').first()
            next_no = (int(last.batch_number[1:]) + 1) if last else 1

            # ✅ Ensure uniqueness
            while True:
                candidate = f"B{str(next_no).zfill(3)}"
                if not MedicineBatch.objects.filter(batch_number=candidate).exists():
                    break
                next_no += 1

            self.batch_number = candidate

        is_new = self.pk is None

        self.full_clean()
        super().save(*args, **kwargs)

        # ✅ Stock log only on creation
        if is_new:
            MedicineStockLog.objects.create(
                batch=self,
                change_type='ADD',
                quantity_changed=self.quantity
            )

    def __str__(self):
        return f"{self.medicine.name} - {self.batch_number}"


# ------------------------------
# Stock Log
# ------------------------------
class MedicineStockLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    batch = models.ForeignKey(MedicineBatch, on_delete=models.CASCADE, related_name="logs")

    change_type = models.CharField(max_length=20, choices=[
        ('ADD', 'Added'),
        ('DISPENSE', 'Dispensed'),
        ('EXPIRED', 'Expired')
    ])

    quantity_changed = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        if self.quantity_changed == 0:
            raise ValidationError("Cannot be zero")

        if self.change_type == 'ADD' and self.quantity_changed < 0:
            raise ValidationError("ADD must be positive")

        if self.change_type in ['DISPENSE', 'EXPIRED'] and self.quantity_changed > 0:
            raise ValidationError("Must be negative for stock out")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


# ------------------------------
# Dispense
# ------------------------------
class Dispense(models.Model):
    dispense_id = models.AutoField(primary_key=True)

    prescription = models.ForeignKey("doctor.Prescription", on_delete=models.CASCADE)
    patient = models.ForeignKey("reception.Patient", on_delete=models.CASCADE)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    dispense_date = models.DateTimeField(default=timezone.now)

    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    ], default='Pending')

    def clean(self):
        if self.total_amount <= 0:
            raise ValidationError("Must be > 0")

    def __str__(self):
        return f"Dispense {self.dispense_id}"


# ------------------------------
# Dispense Item (ONLY stock deduction happens here)
# ------------------------------
class DispenseItem(models.Model):
    dispense = models.ForeignKey(Dispense, on_delete=models.CASCADE, related_name='items')
    batch = models.ForeignKey(MedicineBatch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.quantity < 1:
            raise ValidationError("Quantity must be at least 1")

        if self.batch.expiry_date < timezone.now().date():
            raise ValidationError("Batch expired")

        if self.quantity > self.batch.quantity:
            raise ValidationError("Not enough stock")

    def save(self, *args, **kwargs):
        self.price = self.batch.medicine.price
        self.full_clean()

        if not self.pk:
            # ✅ ONLY deduction here (fixes your failing test)
            self.batch.quantity -= self.quantity
            self.batch.save(update_fields=['quantity'])

            MedicineStockLog.objects.create(
                batch=self.batch,
                change_type='DISPENSE',
                quantity_changed=-self.quantity
            )

        super().save(*args, **kwargs)


# ------------------------------
# Medicine Bill
# ------------------------------
class MedicineBill(models.Model):
    bill_id = models.AutoField(primary_key=True)

    dispense = models.OneToOneField(Dispense, on_delete=models.CASCADE)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    payment_status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Paid', 'Paid')
    ], default='Pending')

    created_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        if self.total_amount <= 0:
            raise ValidationError("Total must be > 0")

        if self.discount < 0:
            raise ValidationError("Discount cannot be negative")

        if self.discount > self.total_amount:
            raise ValidationError("Invalid discount")

        if self.dispense and self.total_amount != self.dispense.total_amount:
            raise ValidationError("Must match dispense total")

    def save(self, *args, **kwargs):
        self.full_clean()
        self.final_amount = self.total_amount - self.discount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill {self.bill_id}"