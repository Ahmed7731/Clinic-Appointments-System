# Clinic Appointments System — Class Diagram & Analysis

## Candidate Domain Classes Table

| Category | Classes |
| :--- | :--- |
| **Explicit** | `Patient`, `Doctor`, `AuthorizedClinicStaff`, `Appointment` |
| **Inferred** | `TimeSlot`, `MedicalRecord`, `AppointmentStatus`, `SystemController` |
| **Rejected** | `Payment`, `Invoice`, `Notification`, `Prescription` |

---

## Mermaid Class Diagram

```mermaid
classDiagram
    direction TB

    class Patient {
        +viewDoctorAvailability()
        +bookAppointment()
    }

    class Doctor {
        +getAvailableTimeSlots()
        +acceptAppointment()
        +declineAppointment()
        +viewPendingRequests()
    }

    class Appointment {
        +status : AppointmentStatus
        +createRequest()
        +updateStatus()
    }

    class TimeSlot {
        +isAvailable : Boolean
    }

    class MedicalRecord {
        +data : String
    }

    class AuthorizedClinicStaff {
        +accessMedicalData()
    }

    class SystemController {
        +checkSlotAvailability()
        +checkUpcomingAppointments()
        +verifyStaffAuthorization()
    }

    class AppointmentStatus {
        <<enumeration>>
        Pending
        Accepted
        Declined
    }

    Patient "1" --> "0..*" Appointment : books
    Doctor "1" --> "0..*" Appointment : receives
    Doctor "1" --> "0..*" TimeSlot : offers
    Appointment "1" --> "1" TimeSlot : reserves
    Patient "1" --> "1" MedicalRecord : has
    AuthorizedClinicStaff "0..*" --> "0..*" MedicalRecord : accesses
    SystemController "1" --> "0..*" AuthorizedClinicStaff : verifies
    SystemController "1" --> "0..*" Patient : validates
    SystemController "1" --> "0..*" Doctor : validates
    SystemController "1" --> "0..*" Appointment : checks
    Appointment "1" --> "1" AppointmentStatus : has

    note for Patient "Max Upcoming Appointments Constraint:\n{self.appointments->select(a | a.status = 'Pending' or a.status = 'Accepted')->size() <= N}"
    note for MedicalRecord "Authorization Constraint:\nstaff.isAuthorized == true"
    note for Appointment "Time Slot Availability Constraint:\nSlot must be available when created"
```

---

## Business Constraints & Multiplicities

1. **Appointment Status Constraint:**
   - Managed via the `AppointmentStatus` enumeration (`Pending`, `Accepted`, `Declined`).
2. **Maximum Upcoming Appointments Constraint (OCL):**
   - `{self.appointments->select(a | a.status = 'Pending' or a.status = 'Accepted')->size() <= N}` applied to `Patient` to meet Requirement R4.
3. **Authorization Constraint:**
   - Access to `MedicalRecord` requires staff permission validation (`staff.isAuthorized == true`).
4. **Time Slot Availability Constraint:**
   - An `Appointment` can only reserve a `TimeSlot` if `TimeSlot.isAvailable == true`.