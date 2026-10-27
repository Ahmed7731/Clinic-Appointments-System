# Clinic Appointments — Use Cases

## 1. Actors

- **Patient:** Views doctors' availability and requests appointments.
- **Doctor:** Reviews appointment requests and accepts or declines them.
- **Authorized Clinic Staff:** Accesses patient medical data when authorized.

## 2. Use Cases

### UC-01: View Doctor Availability

**Primary Actor:** Patient

**Preconditions:**
- The patient can access the appointment page.

**Main Flow:**
1. The patient opens the appointment page.
2. The system displays the available doctors.
3. The patient selects a doctor.
4. The system displays the doctor's available days and time slots.
5. The patient views the available appointment times.

**Alternative Flows:**

**A1: No Available Time Slots**
- **4a.** The system finds that the doctor has no available time slots.
- **4b.** The system displays a message informing the patient that no appointments are currently available.

**A2: Availability Cannot Be Loaded**
- **4a.** The system fails to retrieve the doctor's availability.
- **4b.** The system displays an error message.
- **4c.** The patient retries loading the available time slots.

**Postconditions:**
- The patient can view the selected doctor's available appointment times if the operation succeeds.

### UC-02: Book an Appointment

**Primary Actor:** Patient

**Preconditions:**
- The patient has selected a doctor.
- The selected time slot is available.
- The patient has fewer than 3 upcoming appointments.

**Main Flow:**
1. The patient views the doctor's available time slots.
2. The patient selects a time slot.
3. The system checks that the selected slot is still available.
4. The system checks the number of the patient's upcoming appointments.
5. The system creates an appointment request with the status `Pending`.
6. The system informs the patient that the request was submitted successfully.

**Alternative Flows:**

**A1: Selected Time Slot Is No Longer Available**
- **3a.** The system finds that the selected time slot is no longer available.
- **3b.** The system informs the patient that the slot cannot be booked.
- **3c.** The system displays the currently available time slots.
- **3d.** The patient selects another time slot and returns to step 2, or exit.

**A2: Required Information Is Missing**
- **5a.** Before creating the appointment request, the system detects that required booking information is missing.
- **5b.** The system informs the patient which information is required.
- **5c.** The patient provides the missing information.
- **5d.** The system validates the information and continues from step 3 of the main flow.
- **5e.** If the information remains incomplete or invalid, the system displays an error and allows the patient to try again.

**Postconditions:**
- A valid appointment request is saved with the status `Pending`.
- The appointment is not confirmed until the doctor accepts the request.

### UC-03: Accept or Decline an Appointment Request

**Primary Actor:** Doctor

**Preconditions:**
- The doctor is authorized to use the application.
- The doctor has at least one pending appointment request.

**Main Flow:**
1. The doctor opens the appointment requests page.
2. The system displays the doctor's pending appointment requests.
3. The doctor selects an appointment request.
4. The system displays the appointment details.
5. The doctor chooses to accept or decline the request.
6. The system updates the appointment status to `Accepted` or `Declined`.
7. The system displays the updated appointment status.

**Alternative Flows:**

**A1: Request Already Processed**
- **3a.** The system finds that the selected request has already been processed.
- **3b.** The system displays the current appointment status.

**Postconditions:**
- The appointment request has the status `Accepted` or `Declined`, unless it was already processed.

### UC-04: Access Patient Medical Data

**Primary Actor:** Authorized Clinic Staff

**Preconditions:**
- The staff member is authenticated.
- The staff member has permission to access the requested patient's medical data.

**Main Flow:**
1. The staff member opens the patient records section.
2. The system verifies the staff member's identity and authorization.
3. The staff member selects a patient record.
4. The system displays the medical data the staff member is authorized to access.

**Alternative Flows:**

**A1: Patient Record Does Not Exist**
- **3a.** The system cannot find the selected patient record.
- **3b.** The system displays a message informing the staff member that the record does not exist.

**Postconditions:**
- Patient medical data is displayed.

## 3. Requirement Coverage

| Requirement | Description | Use Case |
|---|---|---|
| R1 | Patients can view doctors' available days and times. | UC-01 |
| R2 | Patients can book appointments during available time slots. | UC-02 |
| R3 | Doctors can accept or decline appointment requests. | UC-03 |
| R4 | Patients can have at most N upcoming appointments. | UC-02 |
| R5 | Patient medical data is accessible only to authorized staff. | UC-04 |
| R6 | Available appointment times are displayed within 2 seconds. | UC-01 |
| R7 | The application is usable on mobile phone screens. | UC-01, UC-02 |
