from django.test import TestCase
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import time, date

from django.contrib.auth.models import User
from administration.models import StaffProfile, DoctorProfile
from reception.models import Patient, Appointment
from doctor.models import Consultation
from labtechnician.models import LabTest


# ----------------------------------------
# Today Appointments Tests
# ----------------------------------------
class TestTodayAppointmentsAPI(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.user = User.objects.create(
            username="doctor1",
            email="doc@test.com"
        )

        self.staff = StaffProfile.objects.create(
            user=self.user,
            role="Doctor",
            phone="+911234567890"
        )

        self.doctor = DoctorProfile.objects.create(
            staff=self.staff,
            specialization="General"
        )

        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            phone="9999999999",
            date_of_birth=date(1995,1,1),
            gender="Male",
            address="Test Address"
        )

        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now().date(),
            appointment_time=time(10,0),
            token_number=1,
            reason="Fever"
        )

        self.client.force_authenticate(user=self.user)

    def test_get_today_appointments(self):

        response = self.client.get("/doctor/today-appointments/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_today_appointments_empty(self):

        Appointment.objects.all().delete()

        response = self.client.get("/doctor/today-appointments/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)


# ----------------------------------------
# Consultation Page Tests
# ----------------------------------------
class TestConsultationPageAPI(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.user = User.objects.create(
            username="doctor1",
            email="doc@test.com"
        )

        self.staff = StaffProfile.objects.create(
            user=self.user,
            role="Doctor",
            phone="+911234567891"
        )

        self.doctor = DoctorProfile.objects.create(
            staff=self.staff,
            specialization="General"
        )

        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            phone="9999999999",
            date_of_birth=date(1995,1,1),
            gender="Male",
            address="Test Address"
        )

        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now().date(),
            appointment_time=time(10,0),
            token_number=1,
            reason="Fever"
        )

        self.client.force_authenticate(user=self.user)

    def test_consultation_page_success(self):

        url = f"/doctor/consultation/{self.appointment.appointment_id}/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_consultation_invalid_appointment(self):

        response = self.client.get("/doctor/consultation/999/")

        self.assertEqual(response.status_code, 404)


# ----------------------------------------
# Create Consultation Tests
# ----------------------------------------
class TestCreateConsultationAPI(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.user = User.objects.create(
            username="doctor1",
            email="doc@test.com"
        )

        self.staff = StaffProfile.objects.create(
            user=self.user,
            role="Doctor",
            phone="+911234567892"
        )

        self.doctor = DoctorProfile.objects.create(
            staff=self.staff,
            specialization="General"
        )

        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            phone="9999999999",
            date_of_birth=date(1995,1,1),
            gender="Male",
            address="Test Address"
        )

        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now().date(),
            appointment_time=time(10,0),
            token_number=1,
            reason="Fever"
        )

        self.client.force_authenticate(user=self.user)

    def test_create_consultation(self):

        data = {
            "appointment": self.appointment.appointment_id,
            "symptoms": "High fever",
            "diagnosis": "Viral fever",
            "vitals": "BP normal",
            "advice": "Rest"
        }

        response = self.client.post("/doctor/consultations/", data)

        self.assertEqual(response.status_code, 201)

    def test_duplicate_consultation(self):

        data = {
            "appointment": self.appointment.appointment_id,
            "symptoms": "High fever",
            "diagnosis": "Viral fever",
            "vitals": "BP normal",
            "advice": "Rest"
        }

        self.client.post("/doctor/consultations/", data)

        response = self.client.post("/doctor/consultations/", data)

        self.assertEqual(response.status_code, 400)


# ----------------------------------------
# Create Lab Test Request Tests
# ----------------------------------------
class TestCreateLabTestRequestAPI(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.user = User.objects.create(
            username="doctor1",
            email="doc@test.com"
        )

        self.staff = StaffProfile.objects.create(
            user=self.user,
            role="Doctor",
            phone="+911234567893"
        )

        self.doctor = DoctorProfile.objects.create(
            staff=self.staff,
            specialization="General"
        )

        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            phone="9999999999",
            date_of_birth=date(1995,1,1),
            gender="Male",
            address="Test Address"
        )

        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now().date(),
            appointment_time=time(10,0),
            token_number=1,
            reason="Fever"
        )

        self.consultation = Consultation.objects.create(
            appointment=self.appointment,
            symptoms="Fever",
            diagnosis="Viral",
            vitals="Normal",
            advice="Rest"
        )

        self.lab_test = LabTest.objects.create(
            test_name="Blood Test",
            cost=500
        )

        self.client.force_authenticate(user=self.user)

    def test_create_lab_request(self):

        data = {
            "consultation": self.consultation.id,
            "doctor": self.doctor.doctor_id,
            "notes": "Check blood infection",
            "tests": [
                {"lab_test": self.lab_test.test_id}
            ]
        }

        response = self.client.post("/doctor/lab-test-request/", data, format="json")

        self.assertEqual(response.status_code, 201)


# ----------------------------------------
# View Lab Results Tests
# ----------------------------------------
class TestViewLabResultsAPI(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.user = User.objects.create(
            username="doctor1",
            email="doc@test.com"
        )

        self.staff = StaffProfile.objects.create(
            user=self.user,
            role="Doctor",
            phone="+911234567894"
        )

        self.doctor = DoctorProfile.objects.create(
            staff=self.staff,
            specialization="General"
        )

        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            phone="9999999999",
            date_of_birth=date(1995,1,1),
            gender="Male",
            address="Test Address"
        )

        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now().date(),
            appointment_time=time(10,0),
            token_number=1,
            reason="Fever"
        )

        self.consultation = Consultation.objects.create(
            appointment=self.appointment,
            symptoms="Fever",
            diagnosis="Viral",
            vitals="Normal",
            advice="Rest"
        )

        self.client.force_authenticate(user=self.user)

    def test_view_lab_results_empty(self):

        url = f"/doctor/lab-results/{self.consultation.id}/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_lab_results_invalid_consultation(self):

        response = self.client.get("/doctor/lab-results/999/")

        self.assertEqual(response.status_code, 404)


# ----------------------------------------
# Create Prescription Tests
# ----------------------------------------
class TestCreatePrescriptionAPI(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.user = User.objects.create(
            username="doctor1",
            email="doc@test.com"
        )

        self.staff = StaffProfile.objects.create(
            user=self.user,
            role="Doctor",
            phone="+911234567895"
        )

        self.doctor = DoctorProfile.objects.create(
            staff=self.staff,
            specialization="General"
        )

        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            phone="9999999999",
            date_of_birth=date(1995,1,1),
            gender="Male",
            address="Test Address"
        )

        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now().date(),
            appointment_time=time(10,0),
            token_number=1,
            reason="Fever"
        )

        self.consultation = Consultation.objects.create(
            appointment=self.appointment,
            symptoms="Fever",
            diagnosis="Viral",
            vitals="Normal",
            advice="Rest"
        )

        self.client.force_authenticate(user=self.user)

    def test_create_prescription(self):

        data = {
            "consultation": self.consultation.id,
            "doctor": self.doctor.doctor_id,
            "items": [
                {
                    "medicine_name": "Paracetamol",
                    "dosage": "500mg",
                    "frequency": "2 times",
                    "duration": 5
                }
            ]
        }

        response = self.client.post("/doctor/prescriptions/", data, format="json")

        self.assertEqual(response.status_code, 201)