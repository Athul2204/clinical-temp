
        


# from django.test import TestCase
# from django.contrib.auth.models import User, Group
# from django.utils import timezone
# from rest_framework.test import APIClient
# from rest_framework import status
# from decimal import Decimal
# from datetime import date, timedelta

# from pharmacist.models import Medicine, MedicineBatch, MedicineStockLog, Dispense, MedicineBill
# from doctor.models import Prescription, Consultation, PrescriptionItem
# from reception.models import Patient, Appointment
# from administration.models import DoctorProfile, StaffProfile


# # ================================
# # BASE SETUP
# # ================================

# class BaseTestSetup(TestCase):

#     def setUp(self):

#         # Pharmacist user
#         pharmacist_group, _ = Group.objects.get_or_create(name='Pharmacist')
#         self.pharmacist_user = User.objects.create_user(
#             username='pharmacist1',
#             password='test1234'
#         )
#         self.pharmacist_user.groups.add(pharmacist_group)

#         # Doctor user
#         doctor_group, _ = Group.objects.get_or_create(name='Doctor')
#         self.doctor_user = User.objects.create_user(
#             username='doctor1',
#             password='test1234'
#         )
#         self.doctor_user.groups.add(doctor_group)

#         # Staff Profile for doctor
#         self.staff = StaffProfile.objects.create(
#             user=self.doctor_user,
#             role='Doctor',
#             phone='9876543210',
#             date_of_birth=date(1985, 1, 1),
#             address='123 Street'
#         )

#         # Doctor Profile
#         self.doctor_profile = DoctorProfile.objects.create(
#             staff=self.staff,
#             specialization='General'
#         )

#         # Patient — all required fields provided
#         self.patient = Patient.objects.create(
#             first_name='John',
#             last_name='Doe',
#             email='john@test.com',
#             phone='9000000001',
#             date_of_birth=date(1995, 6, 15),
#             gender='Male',
#             address='Kerala',
#             blood_group='O+'
#         )

#         # Appointment — today's date, future time
#         self.appointment = Appointment.objects.create(
#             patient=self.patient,
#             doctor=self.doctor_profile,
#             appointment_date=timezone.now().date(),
#             appointment_time=(timezone.now() + timedelta(hours=1)).time(),
#             token_number=1,
#             reason='Fever',
#             status='Scheduled'
#         )

#         # Consultation
#         self.consultation = Consultation.objects.create(
#             appointment=self.appointment,
#             symptoms='Fever and cold',
#             diagnosis='Viral fever',
#             vitals='BP: 120/80'
#         )

#         # Medicine
#         self.medicine = Medicine.objects.create(
#             name='Paracetamol',
#             price=Decimal('10.00'),
#             unit='tablet'
#         )

#         # Batch
#         self.batch = MedicineBatch.objects.create(
#             medicine=self.medicine,
#             quantity=100,
#             expiry_date=timezone.now().date() + timedelta(days=365)
#         )

#         # Prescription
#         self.prescription = Prescription.objects.create(
#             consultation=self.consultation,
#             doctor=self.doctor_profile,
#             status='Sent',
#             sent_at=timezone.now()
#         )

#         # Prescription Item
#         self.prescription_item = PrescriptionItem.objects.create(
#             prescription=self.prescription,
#             medicine_name=self.medicine,
#             dosage='500mg',
#             frequency='Twice daily',
#             duration=5,
#             instructions='After food'
#         )

#         # API Client
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.pharmacist_user)


# # ================================
# # MEDICINE TESTS
# # ================================

# class MedicineTest(BaseTestSetup):

#     def test_list_medicines(self):
#         response = self.client.get('/api/pharmacist/medicines/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_create_medicine(self):
#         data = {'name': 'Amoxicillin', 'price': '25.00', 'unit': 'capsule'}
#         response = self.client.post('/api/pharmacist/medicines/', data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_create_medicine_invalid_price(self):
#         data = {'name': 'BadMed', 'price': '0.00', 'unit': 'tablet'}
#         response = self.client.post('/api/pharmacist/medicines/', data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_unauthenticated_denied(self):
#         self.client.force_authenticate(user=None)
#         response = self.client.get('/api/pharmacist/medicines/')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_medicine_str(self):
#         self.assertEqual(str(self.medicine), 'Paracetamol')


# # ================================
# # BATCH TESTS
# # ================================

# class MedicineBatchTest(BaseTestSetup):

#     def test_create_batch(self):
#         data = {
#             'medicine': self.medicine.medicine_id,
#             'quantity': 50,
#             'expiry_date': str(timezone.now().date() + timedelta(days=200))
#         }
#         response = self.client.post('/api/pharmacist/batches/', data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_batch_expired_date_fails(self):
#         data = {
#             'medicine': self.medicine.medicine_id,
#             'quantity': 50,
#             'expiry_date': str(timezone.now().date() - timedelta(days=1))
#         }
#         response = self.client.post('/api/pharmacist/batches/', data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_batch_number_auto_generated(self):
#         self.assertTrue(self.batch.batch_number.startswith('B'))

#     def test_stock_log_created_on_batch(self):
#         log = MedicineStockLog.objects.filter(
#             batch=self.batch, change_type='ADD'
#         ).first()
#         self.assertIsNotNone(log)
#         self.assertEqual(log.quantity_changed, 100)


# # ================================
# # INCOMING PRESCRIPTION TESTS
# # ================================

# class IncomingPrescriptionTest(BaseTestSetup):

#     def test_list_sent_prescriptions(self):
#         response = self.client.get('/api/pharmacist/incoming-prescriptions/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['count'], 1)

#     def test_draft_not_visible(self):
#         # Change to Draft — should not appear in list
#         self.prescription.status = 'Draft'
#         self.prescription.save(update_fields=['status'])
#         response = self.client.get('/api/pharmacist/incoming-prescriptions/')
#         self.assertEqual(response.data['count'], 0)

#     def test_prescription_detail(self):
#         response = self.client.get(
#             f'/api/pharmacist/incoming-prescriptions/{self.prescription.prescription_code}/'
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('patient_name', response.data['data'])
#         self.assertIn('items', response.data['data'])

#     def test_invalid_prescription_code(self):
#         response = self.client.get('/api/pharmacist/incoming-prescriptions/PR-999/')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# # ================================
# # DISPENSE TESTS
# # ================================

# class DispenseTest(BaseTestSetup):

#     def get_dispense_data(self):
#         return {
#             'prescription': self.prescription.id,
#             'items': [{'batch': self.batch.batch_id, 'quantity': 10}]
#         }

#     def test_dispense_success(self):
#         response = self.client.post(
#             '/api/pharmacist/dispenses/',
#             self.get_dispense_data(),
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_prescription_becomes_dispensed(self):
#         self.client.post(
#             '/api/pharmacist/dispenses/',
#             self.get_dispense_data(),
#             format='json'
#         )
#         self.prescription.refresh_from_db()
#         self.assertEqual(self.prescription.status, 'Dispensed')

#     def test_stock_reduced_after_dispense(self):
#         self.client.post(
#             '/api/pharmacist/dispenses/',
#             self.get_dispense_data(),
#             format='json'
#         )
#         self.batch.refresh_from_db()
#         self.assertEqual(self.batch.quantity, 90)

#     def test_duplicate_dispense_fails(self):
#         self.client.post(
#             '/api/pharmacist/dispenses/',
#             self.get_dispense_data(),
#             format='json'
#         )
#         response = self.client.post(
#             '/api/pharmacist/dispenses/',
#             self.get_dispense_data(),
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_medicine_not_in_prescription_fails(self):
#         other_medicine = Medicine.objects.create(
#             name='Ibuprofen', price=Decimal('20.00')
#         )
#         other_batch = MedicineBatch.objects.create(
#             medicine=other_medicine,
#             quantity=50,
#             expiry_date=timezone.now().date() + timedelta(days=100)
#         )
#         data = {
#             'prescription': self.prescription.id,
#             'items': [{'batch': other_batch.batch_id, 'quantity': 5}]
#         }
#         response = self.client.post(
#             '/api/pharmacist/dispenses/', data, format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# # ================================
# # BILL TESTS
# # ================================

# class MedicineBillTest(BaseTestSetup):

#     def setUp(self):
#         super().setUp()
#         self.dispense = Dispense.objects.create(
#             prescription=self.prescription,
#             patient=self.patient,
#             total_amount=Decimal('100.00'),
#             status='Completed'
#         )

#     def get_bill_data(self):
#         return {
#             'dispense': self.dispense.dispense_id,
#             'total_amount': '100.00',
#             'discount': '0.00',
#             'payment_status': 'Pending'
#         }

#     def test_create_bill(self):
#         response = self.client.post('/api/pharmacist/bills/', self.get_bill_data())
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_final_amount_correct(self):
#         data = self.get_bill_data()
#         data['discount'] = '10.00'
#         response = self.client.post('/api/pharmacist/bills/', data)
#         self.assertEqual(
#             Decimal(response.data['data']['final_amount']),
#             Decimal('90.00')
#         )

#     def test_duplicate_bill_fails(self):
#         self.client.post('/api/pharmacist/bills/', self.get_bill_data())
#         response = self.client.post('/api/pharmacist/bills/', self.get_bill_data())
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_discount_exceeds_total_fails(self):
#         data = self.get_bill_data()
#         data['discount'] = '200.00'
#         response = self.client.post('/api/pharmacist/bills/', data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from datetime import date, timedelta

from pharmacist.models import (
    Medicine, MedicineBatch, MedicineStockLog,
    Dispense, MedicineBill
)
from doctor.models import Prescription, Consultation, PrescriptionItem
from reception.models import Patient, Appointment
from administration.models import DoctorProfile, StaffProfile


# ================================
# BASE SETUP
# ================================

class BaseTestSetup(TestCase):

    def setUp(self):

        # Pharmacist user
        pharmacist_group, _ = Group.objects.get_or_create(name='Pharmacist')
        self.pharmacist_user = User.objects.create_user(
            username='pharmacist1',
            password='test1234'
        )
        self.pharmacist_user.groups.add(pharmacist_group)

        # Doctor user
        doctor_group, _ = Group.objects.get_or_create(name='Doctor')
        self.doctor_user = User.objects.create_user(
            username='doctor1',
            password='test1234'
        )
        self.doctor_user.groups.add(doctor_group)

        # Staff Profile
        self.staff = StaffProfile.objects.create(
            user=self.doctor_user,
            role='Doctor',
            phone='9876543210',
            date_of_birth=date(1985, 1, 1),
            address='123 Street'
        )

        # Doctor Profile
        self.doctor_profile = DoctorProfile.objects.create(
            staff=self.staff,
            specialization='General'
        )

        # Patient
        self.patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@test.com',
            phone='9000000001',
            date_of_birth=date(1995, 6, 15),
            gender='Male',
            address='Kerala',
            blood_group='O+'
        )

        # Appointment
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor_profile,
            appointment_date=timezone.now().date(),
            appointment_time=(timezone.now() + timedelta(hours=1)).time(),
            token_number=1,
            reason='Fever',
            status='Scheduled'
        )

        # Consultation
        self.consultation = Consultation.objects.create(
            appointment=self.appointment,
            symptoms='Fever and cold',
            diagnosis='Viral fever',
            vitals='BP: 120/80'
        )

        # Medicine
        self.medicine = Medicine.objects.create(
            name='Paracetamol',
            price=Decimal('10.00'),
            unit='tablet'
        )

        # Batch (100 qty)
        self.batch = MedicineBatch.objects.create(
            medicine=self.medicine,
            quantity=100,
            expiry_date=timezone.now().date() + timedelta(days=365)
        )

        # Prescription
        self.prescription = Prescription.objects.create(
            consultation=self.consultation,
            doctor=self.doctor_profile,
            status='Sent',
            sent_at=timezone.now()
        )

        # Prescription Item
        self.prescription_item = PrescriptionItem.objects.create(
            prescription=self.prescription,
            medicine_name=self.medicine,
            dosage='500mg',
            frequency='Twice daily',
            duration=5,
            instructions='After food'
        )

        # API Client
        self.client = APIClient()
        self.client.force_authenticate(user=self.pharmacist_user)


# ================================
# MEDICINE TESTS
# ================================

class MedicineTest(BaseTestSetup):

    def test_list_medicines(self):
        response = self.client.get('/api/pharmacist/medicines/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_medicine(self):
        data = {'name': 'Amoxicillin', 'price': '25.00', 'unit': 'capsule'}
        response = self.client.post('/api/pharmacist/medicines/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_medicine_invalid_price(self):
        data = {'name': 'BadMed', 'price': '0.00', 'unit': 'tablet'}
        response = self.client.post('/api/pharmacist/medicines/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_denied(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/pharmacist/medicines/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_medicine_str(self):
        self.assertEqual(str(self.medicine), 'Paracetamol')


# ================================
# BATCH TESTS
# ================================

class MedicineBatchTest(BaseTestSetup):

    def test_create_batch(self):
        data = {
            'medicine': self.medicine.medicine_id,
            'quantity': 50,
            'expiry_date': str(timezone.now().date() + timedelta(days=200))
        }
        response = self.client.post('/api/pharmacist/batches/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_batch_expired_date_fails(self):
        data = {
            'medicine': self.medicine.medicine_id,
            'quantity': 50,
            'expiry_date': str(timezone.now().date() - timedelta(days=1))
        }
        response = self.client.post('/api/pharmacist/batches/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_batch_number_auto_generated(self):
        self.assertTrue(self.batch.batch_number.startswith('B'))

    def test_stock_log_created_on_batch(self):
        log = MedicineStockLog.objects.filter(
            batch=self.batch,
            change_type='ADD'
        ).first()

        self.assertIsNotNone(log)
        self.assertEqual(log.quantity_changed, 100)


# ================================
# INCOMING PRESCRIPTION TESTS
# ================================

class IncomingPrescriptionTest(BaseTestSetup):

    def test_list_sent_prescriptions(self):
        response = self.client.get('/api/pharmacist/incoming-prescriptions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_draft_not_visible(self):
        self.prescription.status = 'Draft'
        self.prescription.save(update_fields=['status'])

        response = self.client.get('/api/pharmacist/incoming-prescriptions/')
        self.assertEqual(response.data['count'], 0)

    def test_prescription_detail(self):
        response = self.client.get(
            f'/api/pharmacist/incoming-prescriptions/{self.prescription.prescription_code}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('patient_name', response.data['data'])
        self.assertIn('items', response.data['data'])

    def test_invalid_prescription_code(self):
        response = self.client.get('/api/pharmacist/incoming-prescriptions/PR-999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ================================
# DISPENSE TESTS
# ================================

class DispenseTest(BaseTestSetup):

    def get_dispense_data(self):
        return {
            'prescription': self.prescription.id,
            'items': [
                {'batch': self.batch.batch_id, 'quantity': 10}
            ]
        }

    def test_dispense_success(self):
        response = self.client.post(
            '/api/pharmacist/dispenses/',
            self.get_dispense_data(),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_prescription_becomes_dispensed(self):
        self.client.post('/api/pharmacist/dispenses/', self.get_dispense_data(), format='json')
        self.prescription.refresh_from_db()
        self.assertEqual(self.prescription.status, 'Dispensed')

    def test_stock_reduced_after_dispense(self):
        self.client.post('/api/pharmacist/dispenses/', self.get_dispense_data(), format='json')
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity, 90)

    def test_duplicate_dispense_fails(self):
        self.client.post('/api/pharmacist/dispenses/', self.get_dispense_data(), format='json')
        response = self.client.post('/api/pharmacist/dispenses/', self.get_dispense_data(), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_medicine_not_in_prescription_fails(self):
        other_medicine = Medicine.objects.create(
            name='Ibuprofen',
            price=Decimal('20.00')
        )

        other_batch = MedicineBatch.objects.create(
            medicine=other_medicine,
            quantity=50,
            expiry_date=timezone.now().date() + timedelta(days=100)
        )

        data = {
            'prescription': self.prescription.id,
            'items': [{'batch': other_batch.batch_id, 'quantity': 5}]
        }

        response = self.client.post('/api/pharmacist/dispenses/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ================================
# BILL TESTS
# ================================

class MedicineBillTest(BaseTestSetup):

    def setUp(self):
        super().setUp()

        self.dispense = Dispense.objects.create(
            prescription=self.prescription,
            patient=self.patient,
            total_amount=Decimal('100.00'),
            status='Completed'
        )

    def get_bill_data(self):
        return {
            'dispense': self.dispense.dispense_id,
            'total_amount': '100.00',
            'discount': '0.00',
            'payment_status': 'Pending'
        }

    def test_create_bill(self):
        response = self.client.post('/api/pharmacist/bills/', self.get_bill_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_final_amount_correct(self):
        data = self.get_bill_data()
        data['discount'] = '10.00'

        response = self.client.post('/api/pharmacist/bills/', data)

        self.assertEqual(
            Decimal(response.data['data']['final_amount']),
            Decimal('90.00')
        )

    def test_duplicate_bill_fails(self):
        self.client.post('/api/pharmacist/bills/', self.get_bill_data())
        response = self.client.post('/api/pharmacist/bills/', self.get_bill_data())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_discount_exceeds_total_fails(self):
        data = self.get_bill_data()
        data['discount'] = '200.00'

        response = self.client.post('/api/pharmacist/bills/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)