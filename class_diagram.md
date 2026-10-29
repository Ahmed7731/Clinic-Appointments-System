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
        +id : String
        +name : String
        +viewDoctorAvailability()
        +bookAppointment()
    }

    class Doctor {
        +id : String
        +name : String
        +specialty : String
        +getAvailableTimeSlots()
        +acceptAppointment()
        +declineAppointment()
        +viewPendingRequests()
    }

    class Appointment {
        +appointmentId : String
        +date : DateTime
        +status : AppointmentStatus
        +createRequest()
        +updateStatus()
    }

    class TimeSlot {
        +slotId : String
        +dateTime : DateTime
        +isAvailable : Boolean
    }

    class MedicalRecord {
        +recordId : String
        +data : String
    }

    class AuthorizedClinicStaff {
        +id : String
        +name : String
        +isAuthorized : Boolean
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
