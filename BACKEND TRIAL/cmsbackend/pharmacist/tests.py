# from django.test import TestCase

# # Create your tests here.
# from rest_framework.test import APITestCase
# from rest_framework import status
# from django.urls import reverse
# from django.utils import timezone
# from datetime import timedelta,date

# from .models import Medicine, MedicineBatch, Dispense, MedicineBill


# # ==============================
# # Medicine API Tests
# # ==============================
# class MedicineAPITest(APITestCase):

#     def setUp(self):
#         self.url = reverse('medicine-list')
#         self.medicine = Medicine.objects.create(
#             name="Paracetamol",
#             price="10.00",
#             unit="tablet"
#         )

#     def test_get_medicines(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

#     def test_post_medicine(self):
#         data = {
#             "name": "Ibuprofen",
#             "price": "15.00",
#             "unit": "tablet"
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Medicine.objects.count(), 2)

#     def test_post_medicine_invalid_price(self):
#         data = {
#             "name": "Ibuprofen",
#             "price": "-5.00",
#             "unit": "tablet"
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_post_medicine_duplicate_name(self):
#         data = {
#             "name": "Paracetamol",
#             "price": "20.00",
#             "unit": "tablet"
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_put_medicine(self):
#         url = reverse('medicine-detail', kwargs={'pk': self.medicine.pk})
#         updated_data = {
#             "name": "Paracetamol 500mg",
#             "price": "20.00",
#             "unit": "tablet"
#         }
#         response = self.client.put(url, updated_data)
#         print(response.status_code)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.medicine.refresh_from_db()
#         self.assertEqual(self.medicine.name, "Paracetamol 500mg")

#     def test_delete_medicine(self):
#         url = reverse('medicine-detail', kwargs={'pk': self.medicine.pk})
#         response = self.client.delete(url)
#         print("STATUS:", response.status_code)
#         print("DATA:", response.data)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Medicine.objects.count(), 0)


# # ==============================
# # Medicine Batch API Tests
# # ==============================
# class MedicineBatchAPITest(APITestCase):

#     def setUp(self):
#         self.url = reverse('batch-list')
#         self.medicine = Medicine.objects.create(
#             name="Paracetamol",
#             price="10.00",
#             unit="tablet"
#         )
#         self.batch = MedicineBatch.objects.create(
#             medicine=self.medicine,
#             batch_number="BATCH001",
#             quantity=100,
#             expiry_date=timezone.now().date() + timedelta(days=365)
#         )

#     def test_get_batches(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

#     def test_post_batch(self):
#         data = {
#             "medicine": self.medicine.medicine_id,
#             "batch_number": "BATCH002",
#             "quantity": 50,
#             "expiry_date": (timezone.now().date() + timedelta(days=365)).isoformat()
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(MedicineBatch.objects.count(), 2)

#     def test_post_batch_past_expiry(self):
#         data = {
#             "medicine": self.medicine.medicine_id,
#             "batch_number": "BATCH003",
#             "quantity": 50,
#             "expiry_date": (timezone.now().date() - timedelta(days=1)).isoformat()
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_post_batch_zero_quantity(self):
#         data = {
#             "medicine": self.medicine.medicine_id,
#             "batch_number": "BATCH004",
#             "quantity": 0,
#             "expiry_date": (timezone.now().date() + timedelta(days=365)).isoformat()
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_post_batch_duplicate(self):
#         data = {
#             "medicine": self.medicine.medicine_id,
#             "batch_number": "BATCH001",
#             "quantity": 50,
#             "expiry_date": (timezone.now().date() + timedelta(days=365)).isoformat()
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_delete_batch(self):
#         url = reverse('batch-detail', kwargs={'pk': self.batch.pk})
#         response = self.client.delete(url)
#         print("STATUS:", response.status_code)
#         print("DATA:", response.data)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(MedicineBatch.objects.count(), 0)


# # ==============================
# # Medicine Bill API Tests
# # ==============================
# class MedicineBillAPITest(APITestCase):

#     def setUp(self):
#         self.url = reverse('medicinebill-list')

#         from django.contrib.auth.models import User
#         from administration.models import StaffProfile, DoctorProfile
#         from reception.models import Patient, Appointment
#         from doctor.models import Consultation, Prescription

#         # Doctor setup
#         self.user = User.objects.create_user(username="doctor1", password="pass")
#         self.staff = StaffProfile.objects.create(user=self.user, role="Doctor")
#         self.doctor = DoctorProfile.objects.create(staff=self.staff)

#         # Patient setup
#         self.patient = Patient.objects.create(
#             first_name="John",
#             last_name="Doe",
#             email="john@example.com",
#             phone="1234567890",
#             # date_of_birth="1990-01-01",
#             date_of_birth=date(1990, 1, 1),
#             gender="Male",
#             address="Test Address"
#         )

#         # Appointment → Consultation → Prescription
#         self.appointment = Appointment.objects.create(
#             patient=self.patient,
#             doctor=self.doctor,
#             appointment_date=timezone.now().date(),
#             appointment_time=timezone.now().time(),
#             token_number=1,
#             reason="Fever",
#             status="Scheduled"
#         )
#         self.consultation = Consultation.objects.create(
#             appointment=self.appointment,
#             diagnosis="Fever"
#         )
#         self.prescription = Prescription.objects.create(
#             consultation=self.consultation
#         )

#         # Dispense created directly
#         self.dispense = Dispense.objects.create(
#             prescription=self.prescription,
#             patient=self.patient,
#             total_amount="50.00",
#             status="Completed"
#         )

#     def test_get_bills(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_post_bill(self):
#         data = {
#             "dispense": self.dispense.dispense_id,
#             "total_amount": "50.00"
#             # discount → defaults to 0
#             # payment_status → defaults to Pending
#         }
#         response = self.client.post(self.url, data)
#         print(response.status_code)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(MedicineBill.objects.count(), 1)

#     def test_post_bill_with_discount(self):
#         data = {
#             "dispense": self.dispense.dispense_id,
#             "total_amount": "50.00",
#             "discount": "10.00"
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # final_amount = 50 - 10 = 40
#         self.assertEqual(float(response.data["data"]["final_amount"]), 40.00)

#     def test_post_bill_discount_exceeds_total(self):
#         data = {
#             "dispense": self.dispense.dispense_id,
#             "total_amount": "50.00",
#             "discount": "100.00"
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_post_bill_total_mismatch(self):
#         data = {
#             "dispense": self.dispense.dispense_id,
#             "total_amount": "999.00"
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_post_bill_duplicate(self):
#         data = {"dispense": self.dispense.dispense_id, "total_amount": "50.00"}
#         self.client.post(self.url, data)
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_delete_bill(self):
#         bill = MedicineBill.objects.create(
#             dispense=self.dispense,
#             total_amount="50.00",
#             discount="0",
#             final_amount="50.00"
#         )
#         url = reverse('medicinebill-detail', kwargs={'pk': bill.pk})
#         response = self.client.delete(url)
#         print("STATUS:", response.status_code)
#         print("DATA:", response.data)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(MedicineBill.objects.count(), 0)
# class DispenseAPITest(APITestCase):

#     def setUp(self):
#         self.url = reverse('dispense-list')

#         from django.contrib.auth.models import User
#         from administration.models import StaffProfile, DoctorProfile
#         from reception.models import Patient, Appointment
#         from doctor.models import Consultation, Prescription

#         # Doctor setup
#         self.user = User.objects.create_user(username="doctor1", password="pass")
#         self.staff = StaffProfile.objects.create(user=self.user, role="Doctor")
#         self.doctor = DoctorProfile.objects.create(staff=self.staff)

#         # Patient setup
#         self.patient = Patient.objects.create(
#             first_name="John",
#             last_name="Doe",
#             email="john@example.com",
#             phone="1234567890",
#             date_of_birth="1990-01-01",
#             gender="Male",
#             address="Test Address"
#         )

#         # Appointment → Consultation → Prescription
#         self.appointment = Appointment.objects.create(
#             patient=self.patient,
#             doctor=self.doctor,
#             appointment_date=timezone.now().date(),
#             appointment_time=timezone.now().time(),
#             token_number=1,
#             reason="Fever",
#             status="Scheduled"
#         )
#         self.consultation = Consultation.objects.create(
#             appointment=self.appointment,
#             diagnosis="Fever"
#         )
#         self.prescription = Prescription.objects.create(
#             consultation=self.consultation
#         )

#         # Medicine and batch
#         self.medicine = Medicine.objects.create(
#             name="Paracetamol",
#             price="10.00",
#             unit="tablet"
#         )
#         self.batch = MedicineBatch.objects.create(
#             medicine=self.medicine,
#             batch_number="BATCH001",
#             quantity=100,
#             expiry_date=timezone.now().date() + timedelta(days=365)
#         )

#     def test_get_dispenses(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_post_dispense(self):
#         data = {
#             "prescription": self.prescription.pk,
#             "items": [
#                 {"batch": self.batch.batch_id, "quantity": 3}
#             ]
#         }
#         response = self.client.post(self.url, data, format="json")
#         print(response.status_code)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Dispense.objects.count(), 1)

#     def test_post_dispense_total_amount_calculated(self):
#         # 5 items x 10.00 = 50.00
#         data = {
#             "prescription": self.prescription.pk,
#             "items": [
#                 {"batch": self.batch.batch_id, "quantity": 5}
#             ]
#         }
#         response = self.client.post(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(float(response.data["data"]["total_amount"]), 50.00)

#     def test_post_dispense_reduces_stock(self):
#         data = {
#             "prescription": self.prescription.pk,
#             "items": [
#                 {"batch": self.batch.batch_id, "quantity": 10}
#             ]
#         }
#         self.client.post(self.url, data, format="json")
#         self.batch.refresh_from_db()
#         self.assertEqual(self.batch.quantity, 90)  # 100 - 10 = 90

#     def test_post_dispense_exceeds_stock(self):
#         data = {
#             "prescription": self.prescription.pk,
#             "items": [
#                 {"batch": self.batch.batch_id, "quantity": 999}
#             ]
#         }
#         response = self.client.post(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_post_dispense_duplicate_prescription(self):
#         data = {
#             "prescription": self.prescription.pk,
#             "items": [
#                 {"batch": self.batch.batch_id, "quantity": 3}
#             ]
#         }
#         self.client.post(self.url, data, format="json")
#         # Try same prescription again
#         response = self.client.post(self.url, data, format="json")
#         print("STATUS:", response.status_code)
#         print("DATA:", response.data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_delete_dispense(self):
#         # Create dispense directly
#         dispense = Dispense.objects.create(
#             prescription=self.prescription,
#             patient=self.patient,
#             total_amount="30.00",
#             status="Completed"
#         )
#         url = reverse('dispense-detail', kwargs={'pk': dispense.pk})
#         response = self.client.delete(url)
#         print("STATUS:", response.status_code)
#         print("DATA:", response.data)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Dispense.objects.count(), 0)


from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .models import Medicine, MedicineBatch, Dispense, MedicineBill


# ==============================
# Medicine API Tests
# ==============================
class MedicineAPITest(APITestCase):

    def setUp(self):
        self.url = reverse('medicine-list')
        self.medicine = Medicine.objects.create(
            name="Paracetamol",
            price="10.00",
            unit="tablet"
        )

    def test_get_medicines(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_medicine(self):
        data = {
            "name": "Ibuprofen",
            "price": "15.00",
            "unit": "tablet"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medicine.objects.count(), 2)

    def test_post_medicine_invalid_price(self):
        data = {
            "name": "Ibuprofen",
            "price": "-5.00",
            "unit": "tablet"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_medicine_duplicate_name(self):
        data = {
            "name": "Paracetamol",
            "price": "20.00",
            "unit": "tablet"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_medicine(self):
        url = reverse('medicine-detail', kwargs={'pk': self.medicine.pk})
        updated_data = {
            "name": "Paracetamol 500mg",
            "price": "20.00",
            "unit": "tablet"
        }
        response = self.client.put(url, updated_data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medicine.refresh_from_db()
        self.assertEqual(self.medicine.name, "Paracetamol 500mg")

    def test_delete_medicine(self):
        url = reverse('medicine-detail', kwargs={'pk': self.medicine.pk})
        response = self.client.delete(url)
        print("STATUS:", response.status_code)
        print("DATA:", response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Medicine.objects.count(), 0)


# ==============================
# Medicine Batch API Tests
# ==============================
class MedicineBatchAPITest(APITestCase):

    def setUp(self):
        self.url = reverse('batch-list')
        self.medicine = Medicine.objects.create(
            name="Paracetamol",
            price="10.00",
            unit="tablet"
        )
        self.batch = MedicineBatch.objects.create(
            medicine=self.medicine,
            batch_number="BATCH001",
            quantity=100,
            expiry_date=timezone.now().date() + timedelta(days=365)
        )

    def test_get_batches(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_batch(self):
        data = {
            "medicine": self.medicine.medicine_id,
            "batch_number": "BATCH002",
            "quantity": 50,
            "expiry_date": (timezone.now().date() + timedelta(days=365)).isoformat()
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MedicineBatch.objects.count(), 2)

    def test_post_batch_past_expiry(self):
        data = {
            "medicine": self.medicine.medicine_id,
            "batch_number": "BATCH003",
            "quantity": 50,
            "expiry_date": (timezone.now().date() - timedelta(days=1)).isoformat()
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_batch_zero_quantity(self):
        data = {
            "medicine": self.medicine.medicine_id,
            "batch_number": "BATCH004",
            "quantity": 0,
            "expiry_date": (timezone.now().date() + timedelta(days=365)).isoformat()
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_batch_duplicate(self):
        data = {
            "medicine": self.medicine.medicine_id,
            "batch_number": "BATCH001",
            "quantity": 50,
            "expiry_date": (timezone.now().date() + timedelta(days=365)).isoformat()
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_batch(self):
        url = reverse('batch-detail', kwargs={'pk': self.batch.pk})
        response = self.client.delete(url)
        print("STATUS:", response.status_code)
        print("DATA:", response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MedicineBatch.objects.count(), 0)


# ==============================
# Medicine Bill API Tests
# ==============================
class MedicineBillAPITest(APITestCase):

    def setUp(self):
        self.url = reverse('medicinebill-list')

        from django.contrib.auth.models import User
        from administration.models import StaffProfile, DoctorProfile
        from reception.models import Patient, Appointment
        from doctor.models import Consultation, Prescription

        # Doctor setup
        self.user = User.objects.create_user(username="doctor1", password="pass")
        self.staff = StaffProfile.objects.create(user=self.user, role="Doctor")
        self.doctor = DoctorProfile.objects.create(staff=self.staff)

        # Patient setup
        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="1234567890",
            date_of_birth="1990-01-01",
            gender="Male",
            address="Test Address"
        )

        # Appointment → Consultation → Prescription
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now().date(),
            appointment_time=timezone.now().time(),
            token_number=1,
            reason="Fever",
            status="Scheduled"
        )
        self.consultation = Consultation.objects.create(
            appointment=self.appointment,
            diagnosis="Fever"
        )
        self.prescription = Prescription.objects.create(
            consultation=self.consultation
        )

        # Dispense created directly
        self.dispense = Dispense.objects.create(
            prescription=self.prescription,
            patient=self.patient,
            total_amount="50.00",
            status="Completed"
        )

    def test_get_bills(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_bill(self):
        data = {
            "dispense": self.dispense.dispense_id,
            "total_amount": "50.00"
            # discount → defaults to 0
            # payment_status → defaults to Pending
        }
        response = self.client.post(self.url, data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MedicineBill.objects.count(), 1)

    def test_post_bill_with_discount(self):
        data = {
            "dispense": self.dispense.dispense_id,
            "total_amount": "50.00",
            "discount": "10.00"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # final_amount = 50 - 10 = 40
        self.assertEqual(float(response.data["data"]["final_amount"]), 40.00)

    def test_post_bill_discount_exceeds_total(self):
        data = {
            "dispense": self.dispense.dispense_id,
            "total_amount": "50.00",
            "discount": "100.00"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_bill_total_mismatch(self):
        data = {
            "dispense": self.dispense.dispense_id,
            "total_amount": "999.00"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_bill_duplicate(self):
        data = {"dispense": self.dispense.dispense_id, "total_amount": "50.00"}
        self.client.post(self.url, data)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_bill(self):
        bill = MedicineBill.objects.create(
            dispense=self.dispense,
            total_amount="50.00",
            discount="0",
            final_amount="50.00"
        )
        url = reverse('medicinebill-detail', kwargs={'pk': bill.pk})
        response = self.client.delete(url)
        print("STATUS:", response.status_code)
        print("DATA:", response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MedicineBill.objects.count(), 0)