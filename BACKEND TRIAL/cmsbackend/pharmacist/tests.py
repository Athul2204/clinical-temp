# from django.test import TestCase
# from rest_framework.test import APIClient
# from django.contrib.auth.models import User, Group
# from django.utils import timezone
# from datetime import timedelta, date

# from administration.models import StaffProfile, DoctorProfile, PharmacistProfile
# from reception.models import Patient, Appointment
# from doctor.models import Consultation, Prescription
# from pharmacist.models import (
#     Medicine, MedicineBatch, Dispense, DispenseItem, MedicineBill
# )


# # ----------------------------------------
# # BASE SETUP (Reusable)
# # ----------------------------------------
# class BaseTestSetup(TestCase):

#     def setUp(self):

#         self.client = APIClient()

#         # User
#         self.user = User.objects.create(username="pharma1")

#         # Group
#         group, _ = Group.objects.get_or_create(name="Pharmacist")
#         self.user.groups.add(group)

#         # Staff
#         self.staff = StaffProfile.objects.create(
#             user=self.user,
#             role="Pharmacist",
#             phone="+911234567890"
#         )

#         # Pharmacist
#         self.pharmacist = PharmacistProfile.objects.create(
#             staff=self.staff
#         )

#         # Doctor Setup (required for prescription)
#         doc_user = User.objects.create(username="doctor1")

#         doc_group, _ = Group.objects.get_or_create(name="Doctor")
#         doc_user.groups.add(doc_group)

#         doc_staff = StaffProfile.objects.create(
#             user=doc_user,
#             role="Doctor",
#             phone="+911111111111"
#         )

#         self.doctor = DoctorProfile.objects.create(
#             staff=doc_staff,
#             specialization="General"
#         )

#         # Patient
#         self.patient = Patient.objects.create(
#             first_name="John",
#             last_name="Doe",
#             phone="9999999999",
#             date_of_birth=date(1995, 1, 1),
#             gender="Male"
#         )

#         # Appointment
#         self.appointment = Appointment.objects.create(
#             patient=self.patient,
#             doctor=self.doctor,
#             appointment_date=timezone.now().date(),
#             appointment_time=timezone.now().time(),
#             token_number=1,
#             reason="Fever"
#         )

#         # Consultation
#         self.consultation = Consultation.objects.create(
#             appointment=self.appointment,
#             symptoms="Fever",
#             diagnosis="Viral",
#             vitals="Normal"
#         )

#         # Prescription
#         self.prescription = Prescription.objects.create(
#             consultation=self.consultation,
#             doctor=self.doctor
#         )

#         self.client.force_authenticate(user=self.user)


# # ----------------------------------------
# # MEDICINE TESTS
# # ----------------------------------------
# class TestMedicineAPI(BaseTestSetup):

#     def test_create_medicine(self):
#         data = {
#             "name": "Paracetamol",
#             "price": 50
#         }

#         response = self.client.post("/pharmacist/medicines/", data)
#         self.assertEqual(response.status_code, 201)

#     def test_duplicate_medicine(self):
#         Medicine.objects.create(name="Paracetamol", price=50)

#         response = self.client.post("/pharmacist/medicines/", {
#             "name": "Paracetamol",
#             "price": 50
#         })

#         self.assertEqual(response.status_code, 400)

#     def test_invalid_price(self):
#         response = self.client.post("/pharmacist/medicines/", {
#             "name": "BadMed",
#             "price": -10
#         })

#         self.assertEqual(response.status_code, 400)


# # ----------------------------------------
# # MEDICINE BATCH TESTS
# # ----------------------------------------
# class TestMedicineBatchAPI(BaseTestSetup):

#     def setUp(self):
#         super().setUp()

#         self.medicine = Medicine.objects.create(
#             name="Paracetamol",
#             price=50
#         )

#     def test_create_batch(self):
#         data = {
#             "medicine": self.medicine.medicine_id,
#             "quantity": 10,
#             "expiry_date": (timezone.now().date() + timedelta(days=10))
#         }

#         response = self.client.post("/pharmacist/batches/", data)
#         self.assertEqual(response.status_code, 201)

#     def test_zero_quantity(self):
#         response = self.client.post("/pharmacist/batches/", {
#             "medicine": self.medicine.medicine_id,
#             "quantity": 0,
#             "expiry_date": (timezone.now().date() + timedelta(days=10))
#         })

#         self.assertEqual(response.status_code, 400)


# # ----------------------------------------
# # DISPENSE TESTS
# # ----------------------------------------
# class TestDispenseAPI(BaseTestSetup):

#     def setUp(self):
#         super().setUp()

#         self.medicine = Medicine.objects.create(
#             name="Paracetamol",
#             price=50
#         )

#         self.batch = MedicineBatch.objects.create(
#             medicine=self.medicine,
#             quantity=10,
#             expiry_date=timezone.now().date() + timedelta(days=10)
#         )

#         self.prescription.status = "Sent"
#         self.prescription.save()

#     def test_create_dispense(self):

#         data = {
#             "prescription": self.prescription.id,
#             "patient": self.patient.id,
#             "total_amount": 100
#         }

#         response = self.client.post("/pharmacist/dispense/", data)
#         self.assertEqual(response.status_code, 201)

#     def test_dispense_item(self):

#         dispense = Dispense.objects.create(
#             prescription=self.prescription,
#             patient=self.patient,
#             total_amount=100
#         )

#         data = {
#             "dispense": dispense.dispense_id,
#             "batch": self.batch.batch_id,
#             "quantity": 2,
#             "price": 50
#         }

#         response = self.client.post("/pharmacist/dispense-items/", data)
#         self.assertEqual(response.status_code, 201)


# # ----------------------------------------
# # BILL TESTS
# # ----------------------------------------
# class TestMedicineBillAPI(BaseTestSetup):

#     def setUp(self):
#         super().setUp()

#         self.prescription.status = "Sent"
#         self.prescription.save()

#         self.dispense = Dispense.objects.create(
#             prescription=self.prescription,
#             patient=self.patient,
#             total_amount=100
#         )

#     def test_create_bill(self):

#         data = {
#             "dispense": self.dispense.dispense_id,
#             "total_amount": 100,
#             "discount": 10
#         }

#         response = self.client.post("/pharmacist/bills/", data)
#         self.assertEqual(response.status_code, 201)

#     def test_discount_exceeds_total(self):

#         response = self.client.post("/pharmacist/bills/", {
#             "dispense": self.dispense.dispense_id,
#             "total_amount": 100,
#             "discount": 200
#         })

#         self.assertEqual(response.status_code, 400)

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import timedelta, date

from administration.models import StaffProfile, DoctorProfile, PharmacistProfile
from reception.models import Patient, Appointment
from doctor.models import Consultation, Prescription
from pharmacist.models import Medicine, MedicineBatch, Dispense, MedicineBill


# ----------------------------------------
# BASE SETUP
# ----------------------------------------
class BaseTestSetup(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Pharmacist user
        self.user = User.objects.create_user(username="pharma1")

        group, _ = Group.objects.get_or_create(name="Pharmacist")
        self.user.groups.add(group)

        self.staff = StaffProfile.objects.create(
            user=self.user,
            role="Pharmacist",
            phone="+911234567890"
        )

        PharmacistProfile.objects.create(staff=self.staff)

        self.client.force_authenticate(user=self.user)

        # Doctor
        doc_user = User.objects.create_user(username="doctor1")

        doc_group, _ = Group.objects.get_or_create(name="Doctor")
        doc_user.groups.add(doc_group)

        doc_staff = StaffProfile.objects.create(
            user=doc_user,
            role="Doctor",
            phone="+911111111111"
        )

        self.doctor = DoctorProfile.objects.create(
            staff=doc_staff,
            specialization="General"
        )

        # Patient
        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            phone="9999999999",
            date_of_birth=date(1995, 1, 1),
            gender="Male"
        )

        # Appointment
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now().date(),
            appointment_time=timezone.now().time(),
            token_number=1,
            reason="Fever"
        )

        # Consultation
        self.consultation = Consultation.objects.create(
            appointment=self.appointment,
            symptoms="Fever",
            diagnosis="Viral",
            vitals="Normal"
        )

        # Prescription
        self.prescription = Prescription.objects.create(
            consultation=self.consultation,
            doctor=self.doctor,
            status="Sent"
        )


# ----------------------------------------
# MEDICINE TESTS
# ----------------------------------------
class TestMedicineAPI(BaseTestSetup):

    def test_create_medicine(self):
        response = self.client.post(
            "/api/pharmacist/medicines/",
            {"name": "Paracetamol", "price": 50}
        )
        self.assertEqual(response.status_code, 201)

    def test_duplicate_medicine(self):
        Medicine.objects.create(name="Paracetamol", price=50)

        response = self.client.post(
            "/api/pharmacist/medicines/",
            {"name": "Paracetamol", "price": 50}
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_price(self):
        response = self.client.post(
            "/api/pharmacist/medicines/",
            {"name": "BadMed", "price": -10}
        )
        self.assertEqual(response.status_code, 400)


# ----------------------------------------
# MEDICINE BATCH TESTS
# ----------------------------------------
class TestMedicineBatchAPI(BaseTestSetup):

    def setUp(self):
        super().setUp()
        self.medicine = Medicine.objects.create(name="Paracetamol", price=50)

    def test_create_batch(self):
        response = self.client.post(
            "/api/pharmacist/batches/",
            {
                "medicine": self.medicine.medicine_id,
                "quantity": 10,
                "expiry_date": (timezone.now().date() + timedelta(days=10))
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_zero_quantity(self):
        response = self.client.post(
            "/api/pharmacist/batches/",
            {
                "medicine": self.medicine.medicine_id,
                "quantity": 0,
                "expiry_date": (timezone.now().date() + timedelta(days=10))
            }
        )
        self.assertEqual(response.status_code, 400)


# ----------------------------------------
# DISPENSE TESTS
# ----------------------------------------
class TestDispenseAPI(BaseTestSetup):

    def setUp(self):
        super().setUp()

        self.medicine = Medicine.objects.create(name="Paracetamol", price=50)

        self.batch = MedicineBatch.objects.create(
            medicine=self.medicine,
            quantity=10,
            expiry_date=timezone.now().date() + timedelta(days=10)
        )

    def test_create_dispense(self):

        data = {
            "prescription": self.prescription.id,
            "items": [
                {
                    "batch": self.batch.batch_id,
                    "quantity": 2
                }
            ]
        }

        response = self.client.post(
            "/api/pharmacist/dispenses/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 201)

    def test_duplicate_dispense(self):

        data = {
            "prescription": self.prescription.id,
            "items": [
                {
                    "batch": self.batch.batch_id,
                    "quantity": 2
                }
            ]
        }

        self.client.post("/api/pharmacist/dispenses/", data, format="json")

        response = self.client.post(
            "/api/pharmacist/dispenses/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 400)


# ----------------------------------------
# BILL TESTS
# ----------------------------------------
class TestMedicineBillAPI(BaseTestSetup):

    def setUp(self):
        super().setUp()

        self.medicine = Medicine.objects.create(name="Paracetamol", price=50)

        self.batch = MedicineBatch.objects.create(
            medicine=self.medicine,
            quantity=10,
            expiry_date=timezone.now().date() + timedelta(days=10)
        )

        # Create dispense first
        data = {
            "prescription": self.prescription.id,
            "items": [
                {
                    "batch": self.batch.batch_id,
                    "quantity": 2
                }
            ]
        }

        res = self.client.post(
            "/api/pharmacist/dispenses/",
            data,
            format="json"
        )

        self.dispense = Dispense.objects.get(
            pk=res.data["data"]["dispense_id"]
        )

    def test_create_bill(self):

        response = self.client.post(
            "/api/pharmacist/bills/",
            {
                "dispense": self.dispense.dispense_id,
                "total_amount": str(self.dispense.total_amount),
                "discount": 10
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)

    def test_discount_exceeds_total(self):

        response = self.client.post(
            "/api/pharmacist/bills/",
            {
                "dispense": self.dispense.dispense_id,
                "total_amount": str(self.dispense.total_amount),
                "discount": 9999
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_duplicate_bill(self):

        data = {
            "dispense": self.dispense.dispense_id,
            "total_amount": str(self.dispense.total_amount)
        }

        self.client.post("/api/pharmacist/bills/", data, format="json")

        response = self.client.post(
            "/api/pharmacist/bills/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 400)