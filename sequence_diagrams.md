# Clinic Appointments — Sequence Diagrams

## UC-01: View Doctor Availability

```mermaid
sequenceDiagram
    autonumber
    actor P as Patient
    participant UI as Appointment Page
    participant S as System
    participant DB as Database

    P->>UI: Open appointment page
    UI->>S: Request doctors list
    S->>DB: Get available doctors
    DB-->>S: Doctors
    S-->>UI: Doctors
    UI-->>P: Display available doctors
    P->>UI: Select a doctor
    UI->>S: Request doctor availability
    S->>DB: Get days and time slots
    alt Availability loaded with slots
        DB-->>S: Available days and time slots
        S-->>UI: Availability
        UI-->>P: Display available days and time slots
    else A1: No available time slots
        DB-->>S: Empty result
        S-->>UI: No slots
        UI-->>P: "No appointments are currently available"
    else A2: Availability cannot be loaded
        DB--xS: Failure
        S-->>UI: Error
        UI-->>P: Display error message
        opt Patient retries
            P->>UI: Retry loading time slots
            UI->>S: Request doctor availability
        end
    end
```

## UC-02: Book an Appointment

```mermaid
sequenceDiagram
    autonumber
    actor P as Patient
    participant UI as Booking Page
    participant S as System
    participant DB as Database

    P->>UI: View doctor's available time slots
    P->>UI: Select a time slot
    UI->>S: Submit booking request
    opt A2: Required information is missing
        S-->>UI: Missing required information
        UI-->>P: Show which information is required
        P->>UI: Provide missing information
        UI->>S: Resubmit booking request
        Note over S: Validate info, continue from slot check<br/>(if still invalid: show error, patient can retry)
    end
    S->>DB: Check slot is still available
    DB-->>S: Slot status
    alt Slot is available
        S->>DB: Count patient's upcoming appointments
        DB-->>S: Count
        S->>DB: Create appointment request (status = Pending)
        DB-->>S: Saved
        S-->>UI: Request submitted
        UI-->>P: Request submitted successfully
    else A1: Slot is no longer available
        S-->>UI: Slot cannot be booked
        UI-->>P: Slot cannot be booked
        S->>DB: Get currently available slots
        DB-->>S: Available slots
        S-->>UI: Available slots
        UI-->>P: Display available time slots
        Note over P,UI: Patient selects another slot (back to step 2) or exits
    end
```

## UC-03: Accept or Decline an Appointment Request

```mermaid
sequenceDiagram
    autonumber
    actor D as Doctor
    participant UI as Requests Page
    participant S as System
    participant DB as Database

    D->>UI: Open appointment requests page
    UI->>S: Request pending appointments
    S->>DB: Get doctor's pending requests
    DB-->>S: Pending requests
    S-->>UI: Pending requests
    UI-->>D: Display pending requests
    D->>UI: Select an appointment request
    UI->>S: Get request details
    S->>DB: Fetch request
    DB-->>S: Request and current status
    alt Request is Pending
        S-->>UI: Appointment details
        UI-->>D: Display appointment details
        D->>UI: Accept or Decline
        UI->>S: Submit decision
        S->>DB: Update status to Accepted / Declined
        DB-->>S: Updated
        S-->>UI: New status
        UI-->>D: Display updated appointment status
    else A1: Request already processed
        S-->>UI: Current status
        UI-->>D: Display current appointment status
    end
```

## UC-04: Access Patient Medical Data

```mermaid
sequenceDiagram
    autonumber
    actor C as Authorized Clinic Staff
    participant UI as Patient Records Page
    participant S as System
    participant A as Auth Service
    participant DB as Database

    C->>UI: Open patient records section
    UI->>S: Request access
    S->>A: Verify identity and authorization
    A-->>S: Authorized
    S-->>UI: Access granted
    UI-->>C: Show patient records
    C->>UI: Select a patient record
    UI->>S: Get patient record
    S->>DB: Fetch record
    alt Record exists
        DB-->>S: Medical data
        S->>S: Filter to data staff is authorized to see
        S-->>UI: Authorized medical data
        UI-->>C: Display medical data
    else A1: Patient record does not exist
        DB-->>S: Not found
        S-->>UI: Record not found
        UI-->>C: "Record does not exist"
    end
```

