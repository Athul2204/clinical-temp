from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from administration.models import DoctorProfile, StaffProfile
from doctor.models import Consultation, LabTestRequest
from reception.models import Appointment, Patient

from labtechnician.models import (
	LabBill,
	LabEquipment,
	LabOrder,
	LabOrderItem,
	LabResult,
	LabTest,
)


class LabTechnicianAPITestBase(TestCase):
	def setUp(self):
		self.client = APIClient()

		self.user = User.objects.create_user(
			username="labtech1",
			email="labtech@test.com",
			password="pass123",
		)
		self.client.force_authenticate(user=self.user)

		self.doctor_user = User.objects.create_user(
			username="doctor1",
			email="doctor@test.com",
			password="pass123",
		)
		self.doctor_staff = StaffProfile.objects.create(
			user=self.doctor_user,
			role="Doctor",
			phone="+911234567890",
		)
		self.doctor = DoctorProfile.objects.create(
			staff=self.doctor_staff,
			specialization="General",
		)

		self.patient = Patient.objects.create(
			first_name="John",
			last_name="Doe",
			email="john@test.com",
			phone="9999999999",
			date_of_birth=date(1995, 1, 1),
			gender="Male",
			address="Test Address",
		)

		self.appointment = Appointment.objects.create(
			patient=self.patient,
			doctor=self.doctor,
			appointment_date=timezone.now().date(),
			appointment_time=timezone.now().time(),
			token_number=1,
			reason="Fever",
		)

		self.consultation = Consultation.objects.create(
			appointment=self.appointment,
			symptoms="Fever",
			diagnosis="Viral fever",
			vitals="Stable",
			advice="Rest",
		)

		self.lab_request = LabTestRequest.objects.create(
			consultation=self.consultation,
			doctor=self.doctor,
			notes="Check infection markers",
		)

		self.lab_test = LabTest.objects.create(
			test_name="Blood Test",
			description="Basic blood work",
			cost="500.00",
			normal_range="4-10",
			unit="mg/dL",
		)

	def create_lab_order(self, order_number="LAB-001", patient=None):
		return LabOrder.objects.create(
			order_number=order_number,
			lab_request=self.lab_request,
			patient=patient or self.patient,
		)

	def create_lab_order_item(self, lab_order=None, lab_test=None):
		return LabOrderItem.objects.create(
			lab_order=lab_order or self.create_lab_order(),
			lab_test=lab_test or self.lab_test,
		)


class TestLabTestAPI(LabTechnicianAPITestBase):
	def test_list_lab_tests(self):
		response = self.client.get("/api/labtechnician/lab-tests/")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data["count"], 1)
		self.assertEqual(len(response.data["data"]), 1)

	def test_create_lab_test(self):
		data = {
			"test_name": "Urine Test",
			"description": "Routine urine analysis",
			"cost": "300.00",
			"normal_range": "Normal",
			"unit": "cells/hpf",
		}

		response = self.client.post("/api/labtechnician/lab-tests/", data)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(LabTest.objects.count(), 2)

	def test_create_lab_test_rejects_duplicate_name(self):
		data = {
			"test_name": "blood test",
			"description": "Duplicate name with different case",
			"cost": "450.00",
			"normal_range": "Normal",
			"unit": "mg/dL",
		}

		response = self.client.post("/api/labtechnician/lab-tests/", data)

		self.assertEqual(response.status_code, 400)


class TestLabOrderAPI(LabTechnicianAPITestBase):
	def test_list_lab_orders(self):
		self.create_lab_order()

		response = self.client.get("/api/labtechnician/lab-orders/")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data["count"], 1)

	def test_list_lab_orders_empty(self):
		response = self.client.get("/api/labtechnician/lab-orders/")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data["count"], 0)


class TestLabOrderItemAPI(LabTechnicianAPITestBase):
	def setUp(self):
		super().setUp()
		self.lab_order = self.create_lab_order()

	def test_create_lab_order_item(self):
		data = {
			"lab_order": self.lab_order.order_id,
			"lab_test": self.lab_test.test_id,
		}

		response = self.client.post("/api/labtechnician/lab-order-items/", data)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(LabOrderItem.objects.count(), 1)

	def test_create_lab_order_item_rejects_duplicate_test(self):
		self.create_lab_order_item(lab_order=self.lab_order)
		data = {
			"lab_order": self.lab_order.order_id,
			"lab_test": self.lab_test.test_id,
		}

		response = self.client.post("/api/labtechnician/lab-order-items/", data)

		self.assertEqual(response.status_code, 400)


class TestLabResultAPI(LabTechnicianAPITestBase):
	def setUp(self):
		super().setUp()
		self.lab_order = self.create_lab_order()
		self.order_item = self.create_lab_order_item(lab_order=self.lab_order)

	def test_create_lab_result_marks_order_and_request_completed(self):
		data = {
			"lab_order_item": self.order_item.order_item_id,
			"result_value": "5.6",
			"remarks": "Within range",
			"is_critical": False,
		}

		response = self.client.post("/api/labtechnician/lab-results/", data)

		self.assertEqual(response.status_code, 201)

		self.lab_order.refresh_from_db()
		self.lab_request.refresh_from_db()

		self.assertEqual(self.lab_order.status, "Completed")
		self.assertEqual(self.lab_request.status, "Completed")
		self.assertIsNotNone(self.lab_request.completed_at)

	def test_create_lab_result_rejects_blank_result_value(self):
		data = {
			"lab_order_item": self.order_item.order_item_id,
			"result_value": "   ",
			"remarks": "Blank result",
			"is_critical": False,
		}

		response = self.client.post("/api/labtechnician/lab-results/", data)

		self.assertEqual(response.status_code, 400)


class TestLabBillAPI(LabTechnicianAPITestBase):
	def setUp(self):
		super().setUp()
		self.lab_order = self.create_lab_order()

	def test_create_lab_bill(self):
		data = {
			"bill_number": "BILL-001",
			"lab_order": self.lab_order.order_id,
			"total_amount": "1000.00",
			"discount": "100.00",
			"payment_status": "Pending",
		}

		response = self.client.post("/api/labtechnician/lab-bills/", data)

		self.assertEqual(response.status_code, 201)

		bill = LabBill.objects.get()
		self.assertEqual(str(bill.final_amount), "900.00")

	def test_create_lab_bill_rejects_invalid_discount(self):
		data = {
			"bill_number": "BILL-002",
			"lab_order": self.lab_order.order_id,
			"total_amount": "1000.00",
			"discount": "1200.00",
			"payment_status": "Pending",
		}

		response = self.client.post("/api/labtechnician/lab-bills/", data)

		self.assertEqual(response.status_code, 400)


class TestLabEquipmentAPI(LabTechnicianAPITestBase):
	def test_create_lab_equipment(self):
		data = {
			"name": "Centrifuge",
			"purchase_date": "2024-01-01",
			"last_service_date": "2024-06-01",
			"status": "Available",
		}

		response = self.client.post("/api/labtechnician/lab-equipment/", data)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(LabEquipment.objects.count(), 1)

	def test_create_lab_equipment_rejects_invalid_service_date(self):
		data = {
			"name": "Microscope",
			"purchase_date": "2024-06-01",
			"last_service_date": "2024-01-01",
			"status": "Available",
		}

		response = self.client.post("/api/labtechnician/lab-equipment/", data)

		self.assertEqual(response.status_code, 400)


class TestLabMaintenanceAPI(LabTechnicianAPITestBase):
	def setUp(self):
		super().setUp()
		self.equipment = LabEquipment.objects.create(
			name="Analyzer",
			purchase_date=date(2024, 1, 1),
			last_service_date=date(2024, 3, 1),
			status="Available",
		)

	def test_create_lab_maintenance(self):
		data = {
			"equipment": self.equipment.equipment_id,
			"service_date": "2024-04-01",
			"technician_name": "Alex",
			"remarks": "Routine maintenance",
			"cost": "250.00",
		}

		response = self.client.post("/api/labtechnician/lab-maintenance/", data)

		self.assertEqual(response.status_code, 201)

	def test_create_lab_maintenance_rejects_service_date_before_purchase(self):
		data = {
			"equipment": self.equipment.equipment_id,
			"service_date": "2023-12-31",
			"technician_name": "Alex",
			"remarks": "Invalid service date",
			"cost": "250.00",
		}

		response = self.client.post("/api/labtechnician/lab-maintenance/", data)

		self.assertEqual(response.status_code, 400)
