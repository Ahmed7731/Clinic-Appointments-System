# Clinic Appointments — Sequence Diagrams

## UC-01: View Doctor Availability

```mermaid
sequenceDiagram
    autonumber
    actor P as Patient
    participant SC as SystemController
    participant D as Doctor
    participant T as TimeSlot

    P->>SC: viewDoctorAvailability()
    SC-->>P: Display available doctors
    P->>SC: Select a doctor
    SC->>D: getAvailableTimeSlots()
    D->>T: check availability
    T-->>D: isAvailable == true
    alt Slots found
        T-->>D: Available time slots
        D-->>SC: Available days and time slots
        SC-->>P: Display available days and time slots
    else A1: No available time slots
        T-->>D: No slots with isAvailable == true
        D-->>SC: Empty list
        SC-->>P: "No appointments are currently available"
    else A2: Availability cannot be loaded
        D--xSC: Failure
        SC-->>P: Display error message
        opt Patient retries
            P->>SC: Retry loading time slots
            SC->>D: getAvailableTimeSlots()
        end
    end
```

## UC-02: Book an Appointment

```mermaid
sequenceDiagram
    autonumber
    actor P as Patient
    participant SC as SystemController
    participant T as TimeSlot
    participant A as Appointment

    P->>SC: bookAppointment()
    SC->>SC: checkSlotAvailability()
    SC->>T: isAvailable
    T-->>SC: true / false
    alt isAvailable == true
        SC->>SC: checkUpcomingAppointments()
        Note over SC,P: Patient's Pending + Accepted appointments must be <= N
        opt A2: Required information is missing
            SC-->>P: Show which information is required
            P->>SC: Provide missing information
            Note over SC,T: Validate, then continue from the slot check (step 2)<br/>If still invalid: show error, patient can try again
        end
        SC->>A: createRequest()
        Note over A,T: Appointment reserves the TimeSlot only if isAvailable == true
        A-->>SC: status = Pending
        SC-->>P: Request submitted successfully
    else A1: Slot is no longer available
        SC-->>P: Slot cannot be booked
        SC-->>P: Display currently available time slots
        Note over P,SC: Patient selects another slot (back to step 1) or exits
    end
```

## UC-03: Accept or Decline an Appointment Request

```mermaid
sequenceDiagram
    autonumber
    actor D as Doctor
    participant SC as SystemController
    participant A as Appointment

    D->>SC: viewPendingRequests()
    SC->>A: status == Pending
    A-->>SC: Pending requests
    SC-->>D: Display pending requests
    D->>SC: Select an appointment request
    SC->>A: status
    A-->>SC: current status
    alt status == Pending
        SC-->>D: Display appointment details
        D->>SC: acceptAppointment() / declineAppointment()
        SC->>A: updateStatus()
        A-->>SC: status = Accepted / Declined
        SC-->>D: Display updated appointment status
    else A1: Request already processed
        SC-->>D: Display current appointment status
    end
```

## UC-04: Access Patient Medical Data

```mermaid
sequenceDiagram
    autonumber
    actor S as AuthorizedClinicStaff
    participant SC as SystemController
    participant M as MedicalRecord

    S->>SC: Open patient records section
    SC->>SC: verifyStaffAuthorization()
    SC-->>S: Access granted
    S->>SC: accessMedicalData()
    SC->>M: data
    alt Record exists
        M-->>SC: Medical data
        SC-->>S: Display the medical data the staff is authorized to access
    else A1: Patient record does not exist
        M-->>SC: Not found
        SC-->>S: "Record does not exist"
    end
```

