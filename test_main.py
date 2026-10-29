import unittest
from main import (
    Patient, 
    Doctor, 
    TimeSlot, 
    AuthorizedClinicStaff, 
    AppointmentStatus
)


class TestClinicAppointmentsSystem(unittest.TestCase):

    def setUp(self):
        """Sets up the initial environment before running each unit test."""
        self.doctor = Doctor("D001", "Dr. Ahmed Khaled", "Pediatrics")
        self.slot1 = TimeSlot("S1", "2026-06-10 10:00 AM", is_available=True)
        self.slot2 = TimeSlot("S2", "2026-06-10 11:00 AM", is_available=True)
        self.slot3 = TimeSlot("S3", "2026-06-11 09:00 AM", is_available=True)
        
        self.doctor.add_time_slot(self.slot1)
        self.doctor.add_time_slot(self.slot2)
        self.doctor.add_time_slot(self.slot3)

        # Patient configured with max_upcoming_appointments N = 2 for constraint testing
        self.patient = Patient("P001", "Mohamed Ali", max_upcoming_appointments=2)

    def test_view_doctor_availability(self):
        """Test R1: Patient can view doctor's available time slots."""
        available_slots = self.patient.view_doctor_availability(self.doctor)
        self.assertEqual(len(available_slots), 3)

    def test_successful_booking_and_doctor_acceptance(self):
        """Test R2 & R3: Successful appointment booking and doctor acceptance."""
        appointment = self.patient.book_appointment(self.doctor, self.slot1, "APP-101")
        
        # Verify initial pending status
        self.assertIsNotNone(appointment)
        self.assertEqual(appointment.status, AppointmentStatus.PENDING)
        self.assertFalse(self.slot1.is_available)

        # Doctor accepts the appointment
        is_accepted = self.doctor.accept_appointment(appointment)
        self.assertTrue(is_accepted)
        self.assertEqual(appointment.status, AppointmentStatus.ACCEPTED)

    def test_doctor_decline_restores_timeslot(self):
        """Test R3: Doctor declining an appointment frees up the time slot."""
        appointment = self.patient.book_appointment(self.doctor, self.slot1, "APP-101")
        self.assertFalse(self.slot1.is_available)

        # Doctor declines the appointment
        is_declined = self.doctor.decline_appointment(appointment)
        self.assertTrue(is_declined)
        self.assertEqual(appointment.status, AppointmentStatus.DECLINED)
        self.assertTrue(self.slot1.is_available)  # Slot must be available again

    def test_max_upcoming_appointments_constraint_r4(self):
        """Test R4: Enforcing the maximum limit N of active/upcoming appointments."""
        # Booking 1 (Active count = 1)
        app1 = self.patient.book_appointment(self.doctor, self.slot1, "APP-101")
        self.assertIsNotNone(app1)

        # Booking 2 (Active count = 2 -> Reached limit N=2)
        app2 = self.patient.book_appointment(self.doctor, self.slot2, "APP-102")
        self.assertIsNotNone(app2)

        # Booking 3 (Should fail because active appointments limit N=2 is exceeded)
        app3 = self.patient.book_appointment(self.doctor, self.slot3, "APP-103")
        self.assertIsNone(app3)

    def test_medical_data_access_authorization_r5(self):
        """Test R5: Patient medical records are accessible only to authorized staff."""
        authorized_staff = AuthorizedClinicStaff("STF-01", "Sara Mahmoud", is_authorized=True)
        unauthorized_staff = AuthorizedClinicStaff("STF-02", "Khaled Osman", is_authorized=False)

        # Authorized staff should succeed
        auth_data = authorized_staff.access_medical_data(self.patient)
        self.assertIsNotNone(auth_data)
        self.assertIn("Mohamed Ali", auth_data)

        # Unauthorized staff should be denied
        unauth_data = unauthorized_staff.access_medical_data(self.patient)
        self.assertIsNone(unauth_data)


if __name__ == "__main__":
    unittest.main()