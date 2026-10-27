```mermaid
flowchart TD
    Patient([Patient])
    Doctor([Doctor])
    Staff([Authorized Clinic Staff])

    subgraph System["Clinic Appointments System"]
        UC1([UC-01: View Doctor Availability])
        UC2([UC-02: Book an Appointment])
        UC3([UC-03: Accept or Decline an Appointment Request])
        UC4([UC-04: Access Patient Medical Data])
    end

    Patient --> UC1
    Patient --> UC2
    Doctor --> UC3
    Staff --> UC4
