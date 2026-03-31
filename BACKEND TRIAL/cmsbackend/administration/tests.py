# from django.test import TestCase
# from rest_framework.test import APIClient
# from django.utils import timezone
# from datetime import time, date, timedelta
# from django.contrib.auth.models import User, Group

# from administration.models import StaffProfile, DoctorProfile
# from reception.models import Patient, Appointment
# from doctor.models import Consultation
# from labtechnician.models import LabTest


# # ----------------------------------------
# # Today Appointments Tests
# # ----------------------------------------
# class TestTodayAppointmentsAPI(TestCase):

#     def setUp(self):

#         self.client = APIClient()

#         # Create User
#         self.user = User.objects.create(
#             username="doctor1",
#             email="doc@test.com"
#         )

#         # 🔥 ADD DOCTOR GROUP FIX
#         doctor_group, _ = Group.objects.get_or_create(name="Doctor")
#         self.user.groups.add(doctor_group)

#         # Create Staff + DoctorProfile
#         self.staff = StaffProfile.objects.create(
#             user=self.user,
#             role="Doctor",
#             phone="+911234567890"
#         )

#         self.doctor = DoctorProfile.objects.create(
#             staff=self.staff,
#             specialization="General"
#         )

#         # Create Patient
#         self.patient = Patient.objects.create(
#             first_name="John",
#             last_name="Doe",
#             email="john@test.com",
#             phone="9999999999",
#             date_of_birth=date(1995, 1, 1),
#             gender="Male",
#             address="Test Address"
#         )

#         # Create Appointment
#         self.appointment = Appointment.objects.create(
#             patient=self.patient,
#             doctor=self.doctor,
#             appointment_date=timezone.now().date(),
#             appointment_time=time(10, 0),
#             token_number=1,
#             reason="Fever"
#         )

#         self.client.force_authenticate(user=self.user)

#     def test_get_today_appointments(self):

#         response = self.client.get("/doctor/today-appointments/")

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data["count"], 1)

#     def test_today_appointments_empty(self):

#         Appointment.objects.all().delete()

#         response = self.client.get("/doctor/today-appointments/")

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data["count"], 0)


# # ----------------------------------------
# # Consultation Page Tests
# # ----------------------------------------
# class TestConsultationPageAPI(TestCase):

#     def setUp(self):

#         self.client = APIClient()

#         self.user = User.objects.create(
#             username="doctor1",
#             email="doc@test.com"
#         )

#         # 🔥 ADD DOCTOR GROUP FIX
#         doctor_group, _ = Group.objects.get_or_create(name="Doctor")
#         self.user.groups.add(doctor_group)

#         self.staff = StaffProfile.objects.create(
#             user=self.user,
#             role="Doctor",
#             phone="+911234567891"
#         )

#         self.doctor = DoctorProfile.objects.create(
#             staff=self.staff,
#             specialization="General"
#         )

#         self.patient = Patient.objects.create(
#             first_name="John",
#             last_name="Doe",
#             email="john@test.com",
#             phone="9999999999",
#             date_of_birth=date(1995, 1, 1),
#             gender="Male",
#             address="Test Address"
#         )

#         self.appointment = Appointment.objects.create(
#             patient=self.patient,
#             doctor=self.doctor,
#             appointment_date=timezone.now().date(),
#             appointment_time=time(10, 0),
#             token_number=1,
#             reason="Fever"
#         )

#         self.client.force_authenticate(user=self.user)

#     def test_consultation_page_success(self):

#         url = f"/doctor/consultation/{self.appointment.appointment_id}/"
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, 200)

#     def test_consultation_invalid_appointment(self):

#         response = self.client.get("/doctor/consultation/999/")
#         self.assertEqual(response.status_code, 404)




# # ----------------------------------------
# # Create Consultation Tests
# # ----------------------------------------
# class TestCreateConsultationAPI(TestCase):

#     def setUp(self):

#         self.client = APIClient()

#         # Create User
#         self.user = User.objects.create(
#             username="doctor1",
#             email="doc@test.com"
#         )

#         # 🔥 ADD DOCTOR GROUP FIX
#         doctor_group, _ = Group.objects.get_or_create(name="Doctor")
#         self.user.groups.add(doctor_group)

#         # Create Staff + DoctorProfile
#         self.staff = StaffProfile.objects.create(
#             user=self.user,
#             role="Doctor",
#             phone="+911234567892"
#         )

#         self.doctor = DoctorProfile.objects.create(
#             staff=self.staff,
#             specialization="General"
#         )

#         # Create Patient
#         self.patient = Patient.objects.create(
#             first_name="John",
#             last_name="Doe",
#             email="john@test.com",
#             phone="9999999999",
#             date_of_birth=date(1995, 1, 1),
#             gender="Male",
#             address="Test Address"
#         )

#         # Create Appointment
#         self.appointment = Appointment.objects.create(
#             patient=self.patient,
#             doctor=self.doctor,
#             appointment_date=timezone.now().date(),
#             appointment_time=time(10, 0),
#             token_number=1,
#             reason="Fever"
#         )

#         self.client.force_authenticate(user=self.user)

#     def test_create_consultation(self):

#         data = {
#             "appointment": self.appointment.appointment_id,
#             "symptoms": "High fever",
#             "diagnosis": "Viral fever",
#             "vitals": "BP normal",
#             "advice": "Rest"
#         }

#         response = self.client.post("/doctor/consultations/", data)

#         self.assertEqual(response.status_code, 201)

#     def test_duplicate_consultation(self):

#         data = {
#             "appointment": self.appointment.appointment_id,
#             "symptoms": "High fever",
#             "diagnosis": "Viral fever",
#             "vitals": "BP normal",
#             "advice": "Rest"
#         }

#         self.client.post("/doctor/consultations/", data)
#         response = self.client.post("/doctor/consultations/", data)

#         self.assertEqual(response.status_code, 400)

#     def test_consultation_cancelled_appointment(self):

#         self.appointment.status = "Cancelled"
#         self.appointment.save()

#         data = {
#             "appointment": self.appointment.appointment_id,
#             "symptoms": "Fever",
#             "diagnosis": "Viral",
#             "vitals": "Normal",
#             "advice": "Rest"
#         }

#         response = self.client.post("/doctor/consultations/", data)

#         self.assertEqual(response.status_code, 400)

#     def test_consultation_not_today(self):

#         self.appointment.appointment_date = timezone.now().date() - timedelta(days=1)
#         self.appointment.save()

#         data = {
#             "appointment": self.appointment.appointment_id,
#             "symptoms": "Fever",
#             "diagnosis": "Viral",
#             "vitals": "Normal",
#             "advice": "Rest"
#         }

#         response = self.client.post("/doctor/consultations/", data)

#         self.assertEqual(response.status_code, 400)


# # ----------------------------------------
# # Create Lab Test Request Tests
# # ----------------------------------------
# class TestCreateLabTestRequestAPI(TestCase):

#     def setUp(self):

#         self.client = APIClient()

#         # Create User
#         self.user = User.objects.create(
#             username="doctor1",
#             email="doc@test.com"
#         )

#         # 🔥 ADD DOCTOR GROUP FIX
#         doctor_group, _ = Group.objects.get_or_create(name="Doctor")
#         self.user.groups.add(doctor_group)

#         # Create Staff + DoctorProfile
#         self.staff = StaffProfile.objects.create(
#             user=self.user,
#             role="Doctor",
#             phone="+911234567893"
#         )

#         self.doctor = DoctorProfile.objects.create(
#             staff=self.staff,
#             specialization="General"
#         )

#         # Create Patient
#         self.patient = Patient.objects.create(
#             first_name="John",
#             last_name="Doe",
#             email="john@test.com",
#             phone="9999999999",
#             date_of_birth=date(1995, 1, 1),
#             gender="Male",
#             address="Test Address"
#         )

#         # Create Appointment
#         self.appointment = Appointment.objects.create(
#             patient=self.patient,
#             doctor=self.doctor,
#             appointment_date=timezone.now().date(),
#             appointment_time=time(10, 0),
#             token_number=1,
#             reason="Fever"
#         )

#         # Create Consultation
#         self.consultation = Consultation.objects.create(
#             appointment=self.appointment,
#             symptoms="Fever",
#             diagnosis="Viral",
#             vitals="Normal",
#             advice="Rest"
#         )

#         # Create Lab Test
#         self.lab_test = LabTest.objects.create(
#             test_name="Blood Test",
#             cost=500
#         )

#         self.client.force_authenticate(user=self.user)

#     def test_create_lab_request(self):

#         data = {
#             "consultation": self.consultation.id,
#             "doctor": self.doctor.doctor_id,
#             "notes": "Check blood infection",
#             "tests": [
#                 {"lab_test": self.lab_test.test_id}
#             ]
#         }

#         response = self.client.post("/doctor/lab-test-request/", data, format="json")

#         self.assertEqual(response.status_code, 201)

#     def test_duplicate_lab_request(self):

#         data = {
#             "consultation": self.consultation.id,
#             "doctor": self.doctor.doctor_id,
#             "notes": "Check infection",
#             "tests": [
#                 {"lab_test": self.lab_test.test_id}
#             ]
#         }

#         self.client.post("/doctor/lab-test-request/", data, format="json")
#         response = self.client.post("/doctor/lab-test-request/", data, format="json")

#         self.assertEqual(response.status_code, 400)

#     def test_lab_request_doctor_mismatch(self):

#         other_user = User.objects.create(username="doc2")

#         # 🔥 ADD DOCTOR GROUP FIX FOR OTHER USER ALSO
#         doctor_group, _ = Group.objects.get_or_create(name="Doctor")
#         other_user.groups.add(doctor_group)

#         other_staff = StaffProfile.objects.create(
#             user=other_user,
#             role="Doctor",
#             phone="+911111111111"
#         )

#         other_doctor = DoctorProfile.objects.create(
#             staff=other_staff,
#             specialization="General"
#         )

#         data = {
#             "consultation": self.consultation.id,
#             "doctor": other_doctor.doctor_id,
#             "notes": "Check infection",
#             "tests": [
#                 {"lab_test": self.lab_test.test_id}
#             ]
#         }

#         response = self.client.post("/doctor/lab-test-request/", data, format="json")

#         self.assertEqual(response.status_code, 400)


# # ----------------------------------------
# # View Lab Results Tests
# # ----------------------------------------
# class TestViewLabResultsAPI(TestCase):

#     def setUp(self):

#         self.client = APIClient()

#         self.user = User.objects.create(
#             username="doctor1",
#             email="doc@test.com"
#         )

#         # 🔥 ADD DOCTOR GROUP FIX
#         doctor_group, _ = Group.objects.get_or_create(name="Doctor")
#         self.user.groups.add(doctor_group)

#         self.staff = StaffProfile.objects.create(
#             user=self.user,
#             role="Doctor",
#             phone="+911234567894"
#         )

#         self.doctor = DoctorProfile.objects.create(
#             staff=self.staff,
#             specialization="General"
#         )

#         self.patient = Patient.objects.create(
#             first_name="John",
#             last_name="Doe",
#             email="john@test.com",
#             phone="9999999999",
#             date_of_birth=date(1995, 1, 1),
#             gender="Male",
#             address="Test Address"
#         )

#         self.appointment = Appointment.objects.create(
#             patient=self.patient,
#             doctor=self.doctor,
#             appointment_date=timezone.now().date(),
#             appointment_time=time(10, 0),
#             token_number=1,
#             reason="Fever"
#         )

#         self.consultation = Consultation.objects.create(
#             appointment=self.appointment,
#             symptoms="Fever",
#             diagnosis="Viral",
#             vitals="Normal",
#             advice="Rest"
#         )

#         self.client.force_authenticate(user=self.user)

#     def test_view_lab_results_empty(self):

#         url = f"/doctor/lab-results/{self.consultation.id}/"
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, 200)

#     def test_lab_results_invalid_consultation(self):

#         response = self.client.get("/doctor/lab-results/999/")
#         self.assertEqual(response.status_code, 404)


# # ----------------------------------------
# # Create Prescription Tests
# # ----------------------------------------
# class TestCreatePrescriptionAPI(TestCase):

#     def setUp(self):

#         self.client = APIClient()

#         # Create User
#         self.user = User.objects.create(
#             username="doctor1",
#             email="doc@test.com"
#         )

#         # 🔥 ADD DOCTOR GROUP FIX
#         doctor_group, _ = Group.objects.get_or_create(name="Doctor")
#         self.user.groups.add(doctor_group)

#         # Create Staff + DoctorProfile
#         self.staff = StaffProfile.objects.create(
#             user=self.user,
#             role="Doctor",
#             phone="+911234567895"
#         )

#         self.doctor = DoctorProfile.objects.create(
#             staff=self.staff,
#             specialization="General"
#         )

#         # Create Patient
#         self.patient = Patient.objects.create(
#             first_name="John",
#             last_name="Doe",
#             email="john@test.com",
#             phone="9999999999",
#             date_of_birth=date(1995, 1, 1),
#             gender="Male",
#             address="Test Address"
#         )

#         # Create Appointment
#         self.appointment = Appointment.objects.create(
#             patient=self.patient,
#             doctor=self.doctor,
#             appointment_date=timezone.now().date(),
#             appointment_time=time(10, 0),
#             token_number=1,
#             reason="Fever"
#         )

#         # Create Consultation
#         self.consultation = Consultation.objects.create(
#             appointment=self.appointment,
#             symptoms="Fever",
#             diagnosis="Viral",
#             vitals="Normal",
#             advice="Rest"
#         )

#         self.client.force_authenticate(user=self.user)

#     def test_create_prescription(self):

#         data = {
#             "consultation": self.consultation.id,
#             "doctor": self.doctor.doctor_id,
#             "items": [
#                 {
#                     "medicine_name": "Paracetamol",
#                     "dosage": "500mg",
#                     "frequency": "2 times",
#                     "duration": 5
#                 }
#             ]
#         }

#         response = self.client.post(
#             "/doctor/prescriptions/",
#             data,
#             format="json"
#         )

#         self.assertEqual(response.status_code, 201)

#     def test_duplicate_prescription(self):

#         data = {
#             "consultation": self.consultation.id,
#             "doctor": self.doctor.doctor_id,
#             "items": [
#                 {
#                     "medicine_name": "Paracetamol",
#                     "dosage": "500mg",
#                     "frequency": "2 times",
#                     "duration": 5
#                 }
#             ]
#         }

#         self.client.post("/doctor/prescriptions/", data, format="json")
#         response = self.client.post("/doctor/prescriptions/", data, format="json")

#         self.assertEqual(response.status_code, 400)

#     def test_prescription_lab_pending(self):

#         from doctor.models import LabTestRequest

#         LabTestRequest.objects.create(
#             consultation=self.consultation,
#             doctor=self.doctor,
#             notes="Test",
#             status="Pending"
#         )

#         data = {
#             "consultation": self.consultation.id,
#             "doctor": self.doctor.doctor_id,
#             "items": [
#                 {
#                     "medicine_name": "Paracetamol",
#                     "dosage": "500mg",
#                     "frequency": "2 times",
#                     "duration": 5
#                 }
#             ]
#         }

#         response = self.client.post(
#             "/doctor/prescriptions/",
#             data,
#             format="json"
#         )

#         self.assertEqual(response.status_code, 400)


from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta
from rest_framework.test import APITestCase

from administration.models import (
    StaffProfile,
    DoctorProfile,
    ReceptionistProfile,
    LabTechnicianProfile,
    PharmacistProfile,
    AuditLog
)

from administration.serializers import (
    StaffProfileSerializer,
    DoctorProfileSerializer
)


# ------------------------------
# USER + STAFF TESTS
# ------------------------------
class StaffProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="Test@1234",
            email="test@example.com"
        )

    def test_create_staff(self):
        staff = StaffProfile.objects.create(
            user=self.user,
            role="Doctor",
            date_of_birth=date.today() - timedelta(days=30 * 365),
            salary=50000
        )

        self.assertIsNotNone(staff.staff_code)
        self.assertTrue(staff.staff_code.startswith("DOC"))

    def test_invalid_dob(self):
        with self.assertRaises(Exception):
            StaffProfile.objects.create(
                user=self.user,
                role="Doctor",
                date_of_birth=date.today() + timedelta(days=1),
                salary=50000
            )

    def test_salary_validation(self):
        with self.assertRaises(Exception):
            StaffProfile.objects.create(
                user=self.user,
                role="Doctor",
                date_of_birth=date.today() - timedelta(days=30 * 365),
                salary=0
            )


# ------------------------------
# DOCTOR PROFILE TESTS
# ------------------------------
class DoctorProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="doctor1",
            password="Test@1234"
        )

        self.staff = StaffProfile.objects.create(
            user=self.user,
            role="Doctor",
            date_of_birth=date.today() - timedelta(days=35 * 365),
            salary=60000
        )

    def test_create_doctor_profile(self):
        doctor = DoctorProfile.objects.create(
            staff=self.staff,
            specialization="Orthopedic",
            consultation_fee=500,
            experience_years=5
        )

        self.assertEqual(doctor.staff.role, "Doctor")

    def test_invalid_role(self):
        user2 = User.objects.create_user(username="rec1", password="Test@1234")

        staff2 = StaffProfile.objects.create(
            user=user2,
            role="Receptionist",
            date_of_birth=date.today() - timedelta(days=25 * 365),
            salary=20000
        )

        doctor = DoctorProfile(
            staff=staff2,
            specialization="General"
        )

        with self.assertRaises(Exception):
            doctor.full_clean()


# ------------------------------
# RECEPTIONIST TESTS
# ------------------------------
class ReceptionistTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="rec", password="123")

        self.staff = StaffProfile.objects.create(
            user=self.user,
            role="Receptionist",
            date_of_birth=date.today() - timedelta(days=25 * 365),
            salary=20000
        )

    def test_receptionist_creation(self):
        rec = ReceptionistProfile.objects.create(staff=self.staff)
        self.assertEqual(rec.staff.role, "Receptionist")


# ------------------------------
# LAB TECHNICIAN TESTS
# ------------------------------
class LabTechnicianTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="lab", password="123")

        self.staff = StaffProfile.objects.create(
            user=self.user,
            role="Lab Technician",
            date_of_birth=date.today() - timedelta(days=28 * 365),
            salary=25000
        )

    def test_labtech_creation(self):
        lab = LabTechnicianProfile.objects.create(
            staff=self.staff,
            certification_details="MLT"
        )

        self.assertEqual(lab.staff.role, "Lab Technician")


# ------------------------------
# PHARMACIST TESTS
# ------------------------------
class PharmacistTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="pharma", password="123")

        self.staff = StaffProfile.objects.create(
            user=self.user,
            role="Pharmacist",
            date_of_birth=date.today() - timedelta(days=30 * 365),
            salary=30000
        )

    def test_pharmacist_creation(self):
        pharma = PharmacistProfile.objects.create(
            staff=self.staff,
            license_number="LIC12345"
        )

        self.assertEqual(pharma.staff.role, "Pharmacist")


# ------------------------------
# AUDIT LOG TESTS
# ------------------------------
class AuditLogTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="123")

    def test_audit_log_creation(self):
        log = AuditLog.objects.create(
            user=self.user,
            module="Staff",
            action="CREATE",
            description="Created staff"
        )

        self.assertEqual(log.action, "CREATE")


# ------------------------------
# SERIALIZER TESTS
# ------------------------------
class StaffSerializerTest(APITestCase):

    def test_create_staff_serializer(self):

        data = {
            "user": {
                "username": "newuser",
                "email": "new@example.com",
                "password": "StrongPass@123"
            },
            "role": "Doctor",
            "date_of_birth": str(date.today() - timedelta(days=30 * 365)),
            "salary": 50000
        }

        serializer = StaffProfileSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        staff = serializer.save()
        self.assertEqual(staff.role, "Doctor")


class DoctorSerializerTest(APITestCase):

    def test_create_doctor_serializer(self):

        data = {
            "staff": {
                "user": {
                    "username": "docserializer",
                    "email": "doc@example.com",
                    "password": "StrongPass@123"
                },
                "role": "Doctor",
                "date_of_birth": str(date.today() - timedelta(days=35 * 365)),
                "salary": 60000
            },
            "specialization": "Cardiology",
            "consultation_fee": 700,
            "experience_years": 5
        }

        serializer = DoctorProfileSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        doctor = serializer.save()
        self.assertEqual(doctor.specialization, "Cardiology")