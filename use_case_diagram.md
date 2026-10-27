# Use Case Diagram: Clinic Appointment System

```mermaid
actor Patient
actor Doctor
actor Staff

rectangle "Clinic Appointment System" {
    usecase "UC-01: View Availability" as UC1
    usecase "UC-02: Book Appointment" as UC2
    usecase "UC-03: Accept/Decline Request" as UC3
    usecase "UC-04: Access Medical Data" as UC4
}

Patient --> UC1
Patient --> UC2

Doctor --> UC1
Doctor --> UC3

Staff --> UC4
