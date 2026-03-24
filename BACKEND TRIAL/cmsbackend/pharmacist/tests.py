


# from rest_framework.test import APITestCase
# from rest_framework import status
# from django.urls import reverse
# from django.utils import timezone
# from datetime import timedelta
# from datetime import date
# from django.contrib.auth.models import User
# from .models import Medicine, MedicineBatch, Dispense, MedicineBill
# from django.contrib.auth.models import User
# from administration.models import StaffProfile, DoctorProfile
# from reception.models import Patient, Appointment
# from doctor.models import Consultation, Prescription

# # ==============================
# # Medicine API Tests
# # ==============================
# class MedicineAPITest(APITestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(username="testuser", password="pass",is_staff=True,        # ✅ ADD THIS
#         is_superuser=True     )
        
#         self.staff = StaffProfile.objects.create(user=self.user, role="Pharmacist")
#         self.client.force_authenticate(user=self.user) 
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
#         self.user = User.objects.create_user(username="testuser", password="pass",is_staff=True,        # ✅ ADD THIS
#         is_superuser=True     ,)
#         self.staff = StaffProfile.objects.create(user=self.user, role="Pharmacist")
#         self.client.force_authenticate(user=self.user) 
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
#         self.user = User.objects.create_user(username="testuser", password="pass",is_staff=True,        # ✅ ADD THIS
#         is_superuser=True     )
#         self.staff = StaffProfile.objects.create(user=self.user, role="Pharmacist")
#         self.client.force_authenticate(user=self.user) 
        

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
#             date_of_birth=date(1990, 1, 1) ,
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
#             diagnosis="Fever",
#             symptoms="Fever and headache",   # ✅ ADD
#             vitals="Normal"
#         )
#         self.prescription = Prescription.objects.create(
#             consultation=self.consultation,
#             doctor=self.doctor
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


from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from pharmacist.models import Medicine, MedicineBatch, Dispense, MedicineBill
from administration.models import PharmacistProfile

from reception.models import Patient, Appointment
from administration.models import  DoctorProfile

from doctor.models import Consultation, Prescription
class BaseTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # ✅ User
        self.user = User.objects.create_user(
            username="pharma",
            password="test123"
        )

        # # ✅ Make pharmacist
        # PharmacistProfile.objects.create(user=self.user)
        staff = StaffProfile.objects.create(user=self.user)
        PharmacistProfile.objects.create(staff=staff)

        # ✅ Authenticate
        self.client.force_authenticate(user=self.user)

        # ✅ Doctor
        self.doctor_user = User.objects.create_user(
            username="doc",
            password="test123"
        )
        self.doctor = DoctorProfile.objects.create(user=self.doctor_user)

        # ✅ Patient
        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe"
        )

        # ✅ Appointment
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date="2025-01-01",
            token_number=1
        )

        # ✅ Consultation (fix validation)
        self.consultation = Consultation.objects.create(
            appointment=self.appointment,
            symptoms="Fever",
            vitals="Normal"
        )

        # ✅ Prescription (fix doctor error)
        self.prescription = Prescription.objects.create(
            consultation=self.consultation,
            doctor=self.doctor
        )
class MedicineAPITest(BaseTestCase):

    def test_get_medicines(self):
        response = self.client.get("/api/medicines")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_medicine(self):
        data = {"name": "Paracetamol", "price": 10}
        response = self.client.post("/api/medicines", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_medicine_invalid_price(self):
        data = {"name": "BadMed", "price": -10}
        response = self.client.post("/api/medicines", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_medicine_duplicate_name(self):
        Medicine.objects.create(name="Paracetamol", price=10)
        data = {"name": "Paracetamol", "price": 20}
        response = self.client.post("/api/medicines", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_medicine(self):
        med = Medicine.objects.create(name="Para", price=10)
        data = {"name": "ParaNew", "price": 20}
        response = self.client.put(f"/api/medicines/{med.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_medicine(self):
        med = Medicine.objects.create(name="Para", price=10)
        response = self.client.delete(f"/api/medicines/{med.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
class MedicineBatchAPITest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.medicine = Medicine.objects.create(name="Paracetamol", price=10)

    def test_get_batches(self):
        response = self.client.get("/api/batches")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_batch(self):
        data = {
            "medicine": self.medicine.id,
            "batch_number": "B001",
            "expiry_date": "2030-01-01",
            "quantity": 100
        }
        response = self.client.post("/api/batches", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_batch_duplicate(self):
        MedicineBatch.objects.create(
            medicine=self.medicine,
            batch_number="B001",
            expiry_date="2030-01-01",
            quantity=100
        )

        data = {
            "medicine": self.medicine.id,
            "batch_number": "B001",
            "expiry_date": "2030-01-01",
            "quantity": 100
        }
        response = self.client.post("/api/batches", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_batch_zero_quantity(self):
        data = {
            "medicine": self.medicine.id,
            "batch_number": "B002",
            "expiry_date": "2030-01-01",
            "quantity": 0
        }
        response = self.client.post("/api/batches", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_batch(self):
        batch = MedicineBatch.objects.create(
            medicine=self.medicine,
            batch_number="B003",
            expiry_date="2030-01-01",
            quantity=10
        )
        response = self.client.delete(f"/api/batches/{batch.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
class MedicineBillAPITest(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.dispense = Dispense.objects.create(
            prescription=self.prescription,
            total_amount=100
        )

    def test_get_bills(self):
        response = self.client.get("/api/bills")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_bill(self):
        data = {
            "dispense": self.dispense.id,
            "total_amount": 100
        }
        response = self.client.post("/api/bills", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_bill_total_mismatch(self):
        data = {
            "dispense": self.dispense.id,
            "total_amount": 50
        }
        response = self.client.post("/api/bills", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_bill_with_discount(self):
        data = {
            "dispense": self.dispense.id,
            "total_amount": 100,
            "discount": 10
        }
        response = self.client.post("/api/bills", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_bill_discount_exceeds_total(self):
        data = {
            "dispense": self.dispense.id,
            "total_amount": 100,
            "discount": 200
        }
        response = self.client.post("/api/bills", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_bill(self):
        bill = MedicineBill.objects.create(
            dispense=self.dispense,
            total_amount=100
        )
        response = self.client.delete(f"/api/bills/{bill.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)