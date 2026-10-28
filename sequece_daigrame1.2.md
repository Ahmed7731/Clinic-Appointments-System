# Clinic Appointments — Sequence Diagrams

## UC-01: View Doctor Availability

```mermaid
sequenceDiagram
    autonumber
    actor P as Patient
    participant Ctrl as SystemController
    participant D as Doctor
    participant TS as TimeSlot

    P->>Ctrl: viewDoctorAvailability()
    Ctrl->>D: getAvailableTimeSlots()
    alt Availability loaded with time slots
        D->>TS: check availability (isAvailable == true)
        TS-->>D: time slots list
        D-->>Ctrl: time slots
        Ctrl-->>P: display available days and time slots
    else A1: No available time slots
        D->>TS: check availability (isAvailable == true)
        TS-->>D: empty list
        D-->>Ctrl: no available slots
        Ctrl-->>P: "No appointments are currently available"
    else A2: Availability cannot be loaded
        D--xCtrl: failure / exception
        Ctrl-->>P: display error message
        opt Patient retries
            P->>Ctrl: viewDoctorAvailability()
        end
    end
```

## UC-02: Book an Appointment

```mermaid
sequenceDiagram
    autonumber
    actor P as Patient
    participant Ctrl as SystemController
    participant TS as TimeSlot
    participant Appt as Appointment

    P->>Ctrl: bookAppointment()
    opt A2: Required information is missing
        Ctrl-->>P: prompt for missing information
        P->>Ctrl: provide missing details
    end

    Ctrl->>TS: checkSlotAvailability()
    alt Slot is available (isAvailable == true)
        Ctrl->>Ctrl: checkUpcomingAppointments()
        alt Upcoming appointments < N
            Ctrl->>Appt: createRequest()
            Appt-->>Ctrl: appointment request created (status = Pending)
            Ctrl-->>P: request submitted successfully
        else Exceeds Max Upcoming Appointments (N)
            Ctrl-->>P: error: maximum upcoming appointments reached
        end
    else A1: Slot is no longer available
        Ctrl-->>P: slot cannot be booked
        Ctrl->>TS: get current available time slots
        TS-->>Ctrl: available time slots
        Ctrl-->>P: display available time slots
    end
```

## UC-03: Accept or Decline an Appointment Request

```mermaid
sequenceDiagram
    autonumber
    actor D as Doctor
    participant Ctrl as SystemController
    participant Appt as Appointment

    D->>Ctrl: viewPendingRequests()
    Ctrl->>Appt: fetch pending requests
    Appt-->>Ctrl: pending requests list
    Ctrl-->>D: display pending requests
    
    alt Doctor accepts request
        D->>Ctrl: acceptAppointment()
        alt Request is Pending
            Ctrl->>Appt: updateStatus(Accepted)
            Appt-->>Ctrl: status updated to Accepted
            Ctrl-->>D: display updated status: Accepted
        else A1: Request already processed
            Appt-->>Ctrl: return current processed status
            Ctrl-->>D: display current appointment status
        end
    else Doctor declines request
        D->>Ctrl: declineAppointment()
        alt Request is Pending
            Ctrl->>Appt: updateStatus(Declined)
            Appt-->>Ctrl: status updated to Declined
            Ctrl-->>D: display updated status: Declined
        else A1: Request already processed
            Appt-->>Ctrl: return current processed status
            Ctrl-->>D: display current appointment status
        end
    end
```

## UC-04: Access Patient Medical Data

```mermaid
sequenceDiagram
    autonumber
    actor Staff as AuthorizedClinicStaff
    participant Ctrl as SystemController
    participant Rec as MedicalRecord

    Staff->>Ctrl: accessMedicalData()
    Ctrl->>Ctrl: verifyStaffAuthorization()
    
    alt Staff is authorized (staff.isAuthorized == true)
        Ctrl->>Rec: fetch medical data
        alt Record exists
            Rec-->>Ctrl: patient medical data
            Ctrl-->>Staff: display authorized medical data
        else A1: Patient record does not exist
            Rec-->>Ctrl: record not found
            Ctrl-->>Staff: "Record does not exist"
        end
    else Staff is unauthorized
        Ctrl-->>Staff: display access denied error
    end
```