from enum import Enum
from typing import List, Optional


class AppointmentStatus(Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    DECLINED = "Declined"


class TimeSlot:
    """represents an available time slot offered by a doctor."""
    def __init__(self, slot_id: str, date_time: str, is_available: bool = True):
        self.slot_id = slot_id
        self.date_time = date_time
        self.is_available = is_available

    def reserve(self) -> bool:
        """reserves the time slot if it is available."""
        if self.is_available:
            self.is_available = False
            return True
        return False


class Appointment:
    """represents an appointment booking between a patient and a doctor."""
    def __init__(self, appointment_id: str, patient: 'Patient', doctor: 'Doctor', time_slot: TimeSlot):
        self.appointment_id = appointment_id
        self.patient = patient
        self.doctor = doctor
        self.time_slot = time_slot
        self.status = AppointmentStatus.PENDING

    def update_status(self, new_status: AppointmentStatus):
        """updates the status of the appointment."""
        self.status = new_status


class Patient:
    """represents a patient in the clinic system with constraint enforcement for max upcoming appointments (r4)."""
    def __init__(self, patient_id: str, name: str, max_upcoming_appointments: int = 3):
        self.patient_id = patient_id
        self.name = name
        self.max_upcoming_appointments = max_upcoming_appointments
        self.appointments: List[Appointment] = []
        self.medical_record_data = f"Confidential medical history for {self.name}"

    def view_doctor_availability(self, doctor: 'Doctor') -> List[TimeSlot]:
        """views available time slots for a specific doctor (r1)."""
        return doctor.get_available_time_slots()

    def count_active_appointments(self) -> int:
        """counts active (pending or accepted) appointments to satisfy constraint r4."""
        return sum(
            1 for a in self.appointments 
            if a.status in [AppointmentStatus.PENDING, AppointmentStatus.ACCEPTED]
        )

    def book_appointment(self, doctor: 'Doctor', time_slot: TimeSlot, appointment_id: str) -> Optional[Appointment]:
        """books an appointment if limits and availability permit (r2, r4)."""
        # enforce max upcoming appointments constraint (r4)
        if self.count_active_appointments() >= self.max_upcoming_appointments:
            print(f"[Error - R4] Patient {self.name} has reached the maximum upcoming appointments limit ({self.max_upcoming_appointments}).")
            return None

        # check time slot availability
        if not time_slot.is_available:
            print(f"[Error] Time slot {time_slot.date_time} is no longer available.")
            return None

        # create appointment request
        if time_slot.reserve():
            appointment = Appointment(appointment_id, self, doctor, time_slot)
            self.appointments.append(appointment)
            doctor.receive_appointment_request(appointment)
            print(f"[Success] Appointment request created successfully for {self.name} with Dr. {doctor.name}. Status: {appointment.status.value}")
            return appointment
        
        return None


class Doctor:
    """represents a doctor who can manage availability and review requests (r3)."""
    def __init__(self, doctor_id: str, name: str, specialty: str):
        self.doctor_id = doctor_id
        self.name = name
        self.specialty = specialty
        self.available_slots: List[TimeSlot] = []
        self.pending_requests: List[Appointment] = []

    def add_time_slot(self, slot: TimeSlot):
        """adds a time slot to the doctor's schedule."""
        if slot.is_available:
            self.available_slots.append(slot)

    def get_available_time_slots(self) -> List[TimeSlot]:
        """returns only unreserved time slots."""
        return [slot for slot in self.available_slots if slot.is_available]

    def receive_appointment_request(self, appointment: Appointment):
        """receives a new appointment request."""
        self.pending_requests.append(appointment)

    def accept_appointment(self, appointment: Appointment) -> bool:
        """accepts a pending appointment request (r3)."""
        if appointment in self.pending_requests:
            appointment.update_status(AppointmentStatus.ACCEPTED)
            self.pending_requests.remove(appointment)
            print(f"[Accepted] Dr. {self.name} accepted appointment {appointment.appointment_id}.")
            return True
        return False

    def decline_appointment(self, appointment: Appointment) -> bool:
        """declines a pending appointment request and frees up the slot (r3)."""
        if appointment in self.pending_requests:
            appointment.update_status(AppointmentStatus.DECLINED)
            self.pending_requests.remove(appointment)
            appointment.time_slot.is_available = True  # make slot available again
            print(f"[Declined] Dr. {self.name} declined appointment {appointment.appointment_id}.")
            return True
        return False


class AuthorizedClinicStaff:
    """represents clinic staff members and verifies data access authorization (r5)."""
    def __init__(self, staff_id: str, name: str, is_authorized: bool = True):
        self.staff_id = staff_id
        self.name = name
        self.is_authorized = is_authorized

    def access_medical_data(self, patient: Patient) -> Optional[str]:
        """accesses patient medical data only if authorized (r5)."""
        if self.is_authorized:
            print(f"[Authorized Access] Staff member {self.name} successfully accessed medical data for {patient.name}.")
            return patient.medical_record_data
        else:
            print(f"[Access Denied - R5] Staff member {self.name} is not authorized to access medical records.")
            return None


class SystemController:
    """system controller to handle validation checks."""
    @staticmethod
    def verify_staff_authorization(staff: AuthorizedClinicStaff) -> bool:
        """verifies if the staff member has valid permissions."""
        return staff.is_authorized


def main():
    print("=== Starting Clinic Appointments System Execution ==\n")

    # setup basic data: doctor and time slots
    doctor = Doctor("D001", "Dr. Ahmed Khaled", "Pediatrics")
    slot1 = TimeSlot("S1", "2026-06-10 10:00 AM", True)
    slot2 = TimeSlot("S2", "2026-06-10 11:00 AM", True)
    slot3 = TimeSlot("S3", "2026-06-11 09:00 AM", True)
    doctor.add_time_slot(slot1)
    doctor.add_time_slot(slot2)
    doctor.add_time_slot(slot3)

    # initialize a patient with a maximum upcoming appointment limit n = 3
    patient = Patient("P001", "Mohamed Ali", max_upcoming_appointments=3)

    print("--- 1. Testing Successful Flow (Booking & Acceptance) ---")
    available_slots = patient.view_doctor_availability(doctor)
    print(f"Available slots for doctor: {len(available_slots)}")

    # book the first appointment
    app1 = patient.book_appointment(doctor, slot1, "APP-101")
    if app1:
        doctor.accept_appointment(app1)

    print("\n--- 2. Testing Alternative / Constraint Flow (Exceeding Limit N) ---")
    # book the second appointment
    app2 = patient.book_appointment(doctor, slot2, "APP-102")
    
    # book the third appointment to reach the limit n = 3
    app3 = patient.book_appointment(doctor, slot3, "APP-103")

    # attempting to book a fourth appointment (should fail due to r4 constraint limit n=3)
    slot4 = TimeSlot("S4", "2026-06-11 02:00 PM", True)
    doctor.add_time_slot(slot4)
    patient.book_appointment(doctor, slot4, "APP-104")

    print("\n--- 3. Testing Medical Data Security & Authorization (R5) ---")
    staff_authorized = AuthorizedClinicStaff("STF-01", "Sara Mahmoud", is_authorized=True)
    staff_unauthorized = AuthorizedClinicStaff("STF-02", "Khaled Osman", is_authorized=False)

    staff_authorized.access_medical_data(patient)
    staff_unauthorized.access_medical_data(patient)

    print("\n=== System Execution Completed Successfully ===")


if __name__ == "__main__":
    main()
