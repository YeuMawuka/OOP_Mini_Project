# Part 4 - Database Design

The database is a single SQLite file (`data/ehr.db`) created automatically by
`database/connection.py`. The schema below is the exact text stored in `database/schema.py`.
Foreign keys are switched on for every connection with `PRAGMA foreign_keys = ON`.

## Complete SQLite Schema

```sql
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL CHECK (length(trim(first_name)) > 0),
    last_name TEXT NOT NULL CHECK (length(trim(last_name)) > 0),
    national_id TEXT NOT NULL UNIQUE,
    date_of_birth TEXT NOT NULL,
    gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female', 'Other')),
    phone TEXT NOT NULL,
    email TEXT NOT NULL DEFAULT '',
    address TEXT NOT NULL DEFAULT '',
    province TEXT NOT NULL CHECK (province IN (
        'Bulawayo', 'Harare', 'Manicaland', 'Mashonaland Central',
        'Mashonaland East', 'Mashonaland West', 'Masvingo',
        'Matabeleland North', 'Matabeleland South', 'Midlands')),
    blood_group TEXT NOT NULL DEFAULT 'Unknown' CHECK (blood_group IN (
        'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', 'Unknown')),
    allergies TEXT NOT NULL DEFAULT '',
    emergency_contact_name TEXT NOT NULL DEFAULT '',
    emergency_contact_phone TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL CHECK (length(trim(first_name)) > 0),
    last_name TEXT NOT NULL CHECK (length(trim(last_name)) > 0),
    national_id TEXT NOT NULL UNIQUE,
    date_of_birth TEXT NOT NULL,
    gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female', 'Other')),
    phone TEXT NOT NULL,
    email TEXT NOT NULL DEFAULT '',
    specialization TEXT NOT NULL,
    license_number TEXT NOT NULL UNIQUE,
    department TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_patients_name ON patients (last_name, first_name);
CREATE INDEX IF NOT EXISTS idx_doctors_specialization ON doctors (specialization);

CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    appointment_date TEXT NOT NULL,
    appointment_time TEXT NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Scheduled'
        CHECK (status IN ('Scheduled', 'Completed', 'Cancelled')),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors (id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_appointments_patient ON appointments (patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_doctor_slot
    ON appointments (doctor_id, appointment_date, appointment_time);

CREATE TABLE IF NOT EXISTS medical_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    appointment_id INTEGER,
    visit_date TEXT NOT NULL,
    diagnosis TEXT NOT NULL,
    treatment TEXT NOT NULL,
    prescription TEXT NOT NULL DEFAULT '',
    notes TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors (id) ON DELETE RESTRICT,
    FOREIGN KEY (appointment_id) REFERENCES appointments (id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_records_patient ON medical_records (patient_id, visit_date);
```

## Entity Relationship Diagram

```text
 patients 1 ----< appointments >---- 1 doctors
    |  1                                  1  |
    |                                        |
    +---< medical_records >-----------------+
                 ^
                 | appointment_id (optional, 0..1)
            appointments
```

## Primary Keys

Every table has `id INTEGER PRIMARY KEY AUTOINCREMENT`. SQLite generates the next number, and
`AUTOINCREMENT` guarantees an ID is never reused after a row is deleted.

## Foreign Keys

| Child table | Column | Parent | On delete | Reason |
| --- | --- | --- | --- | --- |
| `appointments` | `patient_id` | `patients(id)` | `CASCADE` | If a patient is erased, their appointments go with them |
| `appointments` | `doctor_id` | `doctors(id)` | `RESTRICT` | A doctor with bookings cannot be deleted by mistake |
| `medical_records` | `patient_id` | `patients(id)` | `CASCADE` | If a patient is erased, their records go with them |
| `medical_records` | `doctor_id` | `doctors(id)` | `RESTRICT` | Clinical notes must keep the author doctor |
| `medical_records` | `appointment_id` | `appointments(id)` | `SET NULL` | Removing an appointment must never destroy the clinical note; the link just becomes empty |

## Constraints

| Constraint | Where | Purpose |
| --- | --- | --- |
| `NOT NULL` | Every required column | A row cannot be saved without core data |
| `UNIQUE` | `patients.national_id`, `doctors.national_id`, `doctors.license_number` | No duplicate people or licences |
| `CHECK` | `gender`, `province`, `blood_group`, `status`, non-empty names | The database itself rejects impossible values even if Python is bypassed |
| `DEFAULT` | `email`, `address`, `allergies`, `prescription`, `notes`, `status`, `created_at` | Sensible values for optional fields |
| Indexes | `idx_patients_name`, `idx_doctors_specialization`, `idx_appointments_patient`, `idx_appointments_doctor_slot`, `idx_records_patient` | Faster searches, double-booking checks and history queries |

## How the Tables Relate

- **patients to appointments (one to many):** one patient can have many appointments; each appointment belongs to exactly one patient through `appointments.patient_id`.
- **doctors to appointments (one to many):** one doctor can have many appointments; each appointment has exactly one doctor through `appointments.doctor_id`. The index `idx_appointments_doctor_slot` makes the "is this doctor free at this date and time?" query fast.
- **patients to medical_records (one to many):** a patient's medical history is simply all rows of `medical_records` with that `patient_id`, ordered by `visit_date` (index `idx_records_patient`).
- **doctors to medical_records (one to many):** each record names the doctor who wrote it.
- **appointments to medical_records (one to zero-or-one):** a record may point to the appointment during which it was written. The link is optional, because a doctor can also record a walk-in visit. When a record is linked to a scheduled appointment, the service sets that appointment to `Completed`.
- Appointments and medical records are therefore the two *junction-style* tables that connect patients with doctors.

## Business Rules Enforced Above the Database

| Rule | Where |
| --- | --- |
| A doctor cannot have two scheduled appointments at the same date and time | `AppointmentService._ensure_doctor_free` |
| A cancelled or completed appointment cannot be cancelled again | `Appointment.cancel` |
| A medical record cannot be linked to a cancelled appointment or one that belongs to another patient | `MedicalRecordService._check_links` |
| National ID format and licence number format | `Validators.national_id`, `Validators.license_number` |

## Sample Queries Used by the Program

```sql
-- Patient search
SELECT * FROM patients WHERE first_name LIKE ? OR last_name LIKE ?
  OR (first_name || ' ' || last_name) LIKE ? OR national_id LIKE ? OR phone LIKE ?
  ORDER BY last_name, first_name;

-- Patient medical history with doctor names
SELECT m.id, m.visit_date, m.diagnosis, m.treatment, m.prescription,
       d.first_name || ' ' || d.last_name AS doctor_name
FROM medical_records m JOIN doctors d ON d.id = m.doctor_id
WHERE m.patient_id = ? ORDER BY m.visit_date DESC, m.id DESC;

-- Dashboard counts
SELECT COUNT(*) FROM patients;
SELECT status, COUNT(*) FROM appointments GROUP BY status;
```
