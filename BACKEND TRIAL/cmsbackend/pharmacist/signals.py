# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.utils import timezone
# from django.db.models import F
# from .models import MedicineBatch, MedicineStockLog,DispenseItem

# @receiver(post_save, sender=MedicineBatch)
# def batch_added_stock_log(sender, instance, created, **kwargs):
#     if created:
#         MedicineStockLog.objects.create(
#             batch=instance,
#             change_type="ADD",
#             quantity_changed=instance.quantity,
#             remarks="New batch added"
#         )

# @receiver(post_save, sender=DispenseItem)
# def dispense_stock_log(sender, instance, created, **kwargs):
#     if created:
#         # instance.batch.quantity -= instance.quantity
#         # instance.batch.save()
#         MedicineBatch.objects.filter(batch_id=instance.batch.batch_id).update(
#             quantity=F('quantity') - instance.quantity
#         )
#         MedicineStockLog.objects.create(
#             batch=instance.batch,
#             change_type="DISPENSE",
#             quantity_changed=-instance.quantity,
#             remarks="Medicine dispensed"
#         )

# def check_expired_batches():
#     today = timezone.now().date()

#     expired_batches = MedicineBatch.objects.filter(
#         expiry_date__lt=today,
#         quantity__gt=0
#     )

#     for batch in expired_batches:
#         MedicineStockLog.objects.create(
#             batch=batch,
#             change_type="EXPIRED",
#             quantity_changed=-batch.quantity,
#             remarks="Batch expired"
#         )

#         batch.quantity = 0
#         batch.save()


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import MedicineBatch, MedicineStockLog


# ------------------------------
# ⚠️ IMPORTANT:
# Stock log for ADD is already handled in model
# So we DO NOT duplicate it here
# ------------------------------

# ❌ REMOVE batch_added_stock_log (already in model)


# ------------------------------
# ❌ REMOVE THIS COMPLETELY
# ------------------------------
# Dispense stock deduction is already handled in DispenseItem.save()
# DO NOT duplicate here


# ------------------------------
# Expiry Handler (Manual / Cron Job)
# ------------------------------
def check_expired_batches():
    today = timezone.now().date()

    expired_batches = MedicineBatch.objects.filter(
        expiry_date__lt=today,
        quantity__gt=0
    )

    for batch in expired_batches:
        MedicineStockLog.objects.create(
            batch=batch,
            change_type="EXPIRED",
            quantity_changed=-batch.quantity,
            remarks="Batch expired"
        )

        batch.quantity = 0
        batch.save(update_fields=['quantity'])