from django.test import TestCase
from django.utils import timezone
from datetime import date, time, timedelta
from django.core.exceptions import ValidationError

from administration.models import StaffProfile, DoctorProfile
from reception.models import Patient, DoctorAvailability, Appointment, ConsultationBill
from django.contrib.auth.models import User


# ----------------------------------------
# 🔥 COMMON HELPER (IMPORTANT)
# ----------------------------------------
def get_future_time():
    return (timezone.now() + timedelta(hours=1)).time()


# ----------------------------------------
# Patient Model Tests
# ----------------------------------------
class TestPatientModel(TestCase):

    def test_patient_creation_and_age(self):
        patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            phone="9999999999",
            date_of_birth=date(2000, 1, 1),
            gender="Male",
            address="Test Address"
        )

        self.assertIsNotNone(patient.age)
        self.assertEqual(str(patient), "John Doe")

    def test_future_dob_validation(self):
        patient = Patient(
            first_name="John",
            last_name="Doe",
            email="john2@test.com",
            phone="9999999999",
            date_of_birth=date.today() + timedelta(days=1),
            gender="Male",
            address="Test Address"
        )

        with self.assertRaises(ValidationError):
            patient.full_clean()


# ----------------------------------------
# Doctor Availability Tests
# ----------------------------------------
class TestDoctorAvailabilityModel(TestCase):

    def setUp(self):
        user = User.objects.create(username="doc1")
        staff = StaffProfile.objects.create(user=user, role="Doctor", phone="1234567890")
        self.doctor = DoctorProfile.objects.create(staff=staff, specialization="General")

    def test_valid_availability(self):
        availability = DoctorAvailability(
            doctor=self.doctor,
            available_date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0)
        )
        availability.full_clean()

    def test_invalid_time(self):
        availability = DoctorAvailability(
            doctor=self.doctor,
            available_date=date.today(),
            start_time=time(12, 0),
            end_time=time(10, 0)
        )

        with self.assertRaises(ValidationError):
            availability.full_clean()


# ----------------------------------------
# Appointment Model Tests
# ----------------------------------------
class TestAppointmentModel(TestCase):

    def setUp(self):
        user = User.objects.create(username="doc1")
        staff = StaffProfile.objects.create(user=user, role="Doctor", phone="1234567890")
        self.doctor = DoctorProfile.objects.create(staff=staff, specialization="General")

        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            email="john3@test.com",
            phone="9999999999",
            date_of_birth=date(2000, 1, 1),
            gender="Male",
            address="Test Address"
        )

    def test_valid_appointment(self):
        appointment = Appointment(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now().date(),
            appointment_time=get_future_time(),  # ✅ FIX
            token_number=1,
            reason="Fever"
        )
        appointment.full_clean()

    def test_past_date(self):
        appointment = Appointment(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now().date() - timedelta(days=1),
            appointment_time=get_future_time(),
            token_number=1,
            reason="Fever"
        )

        with self.assertRaises(ValidationError):
            appointment.full_clean()

    def test_past_time_today(self):
        appointment = Appointment(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now().date(),
            appointment_time=(timezone.now() - timedelta(hours=1)).time(),
            token_number=1,
            reason="Fever"
        )

        with self.assertRaises(ValidationError):
            appointment.full_clean()


# ----------------------------------------
# Consultation Bill Tests
# ----------------------------------------
class TestConsultationBillModel(TestCase):

    def setUp(self):
        user = User.objects.create(username="doc1")
        staff = StaffProfile.objects.create(user=user, role="Doctor", phone="1234567890")
        self.doctor = DoctorProfile.objects.create(staff=staff, specialization="General")

        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            email="john4@test.com",
            phone="9999999999",
            date_of_birth=date(2000, 1, 1),
            gender="Male",
            address="Test Address"
        )

        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now().date(),
            appointment_time=get_future_time(),  # ✅ FIX
            token_number=1,
            reason="Fever"
        )

    def test_bill_creation(self):
        bill = ConsultationBill.objects.create(
            appointment=self.appointment,
            amount=500
        )

        self.assertEqual(bill.status, "Unpaid")
        self.assertEqual(str(bill), f"Bill {bill.bill_id}")