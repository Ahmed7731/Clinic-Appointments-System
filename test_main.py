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
        "" "sets up the initial environment before running each unit test." ""
        self.doctor = Doctor("D001", "Dr. Ahmed Khaled", "Pediatrics")
        self.slot1 = TimeSlot("S1", "2026-06-10 10:00 AM", is_available=True)
        self.slot2 = TimeSlot("S2", "2026-06-10 11:00 AM", is_available=True)
        self.slot3 = TimeSlot("S3", "2026-06-11 09:00 AM", is_available=True)
        self.slot4 = TimeSlot("S4", "2026-06-11 10:00 AM", is_available=True)
        
        self.doctor.add_time_slot(self.slot1)
        self.doctor.add_time_slot(self.slot2)
        self.doctor.add_time_slot(self.slot3)
        self.doctor.add_time_slot(self.slot4)

        # patient configured with max_upcoming_appointments N=3 for constraint testing
        self.patient = Patient("P001", "Mohamed Ali", max_upcoming_appointments=3)

    def test_view_doctor_availability(self):
        "" "test r1: patient can view doctor's available time slots." ""
        available_slots = self.patient.view_doctor_availability(self.doctor)
        self.assertEqual(len(available_slots), 4)

    def test_successful_booking_and_doctor_acceptance(self):
        "" "test r2 & r3: successful appointment booking and doctor acceptance." ""
        appointment = self.patient.book_appointment(self.doctor, self.slot1, "APP-101")
        
        # verify initial pending status
        self.assertIsNotNone(appointment)
        self.assertEqual(appointment.status, AppointmentStatus.PENDING)
        self.assertFalse(self.slot1.is_available)

        # doctor accepts the appointment
        is_accepted = self.doctor.accept_appointment(appointment)
        self.assertTrue(is_accepted)
        self.assertEqual(appointment.status, AppointmentStatus.ACCEPTED)

    def test_doctor_decline_restores_timeslot(self):
        "" "test r3: doctor declining an appointment frees up the time slot." ""
        appointment = self.patient.book_appointment(self.doctor, self.slot1, "APP-101")
        self.assertFalse(self.slot1.is_available)

        # doctor declines the appointment
        is_declined = self.doctor.decline_appointment(appointment)
        self.assertTrue(is_declined)
        self.assertEqual(appointment.status, AppointmentStatus.DECLINED)
        self.assertTrue(self.slot1.is_available)  # slot must be available again

    def test_max_upcoming_appointments_constraint_r4(self):
        "" "test r4: enforcing the maximum limit n=3 of active/upcoming appointments." ""
        # booking 1 (active count = 1)
        app1 = self.patient.book_appointment(self.doctor, self.slot1, "APP-101")
        self.assertIsNotNone(app1)

        # booking 2 (active count = 2)
        app2 = self.patient.book_appointment(self.doctor, self.slot2, "APP-102")
        self.assertIsNotNone(app2)

        # booking 3 (active count = 3 -> reached limit N=3)
        app3 = self.patient.book_appointment(self.doctor, self.slot3, "APP-103")
        self.assertIsNotNone(app3)

        # booking 4 (should fail because active appointments limit N=3 is exceeded)
        app4 = self.patient.book_appointment(self.doctor, self.slot4, "APP-104")
        self.assertIsNone(app4)

    def test_medical_data_access_authorization_r5(self):
        "" "test r5: patient medical records are accessible only to authorized staff." ""
        authorized_staff = AuthorizedClinicStaff("STF-01", "Sara Mahmoud", is_authorized=True)
        unauthorized_staff = AuthorizedClinicStaff("STF-02", "Khaled Osman", is_authorized=False)

        # authorized staff should succeed
        auth_data = authorized_staff.access_medical_data(self.patient)
        self.assertIsNotNone(auth_data)
        self.assertIn("Mohamed Ali", auth_data)

        # unauthorized staff should be denied
        unauth_data = unauthorized_staff.access_medical_data(self.patient)
        self.assertIsNone(unauth_data)


if __name__ == "__main__":
    unittest.main()
