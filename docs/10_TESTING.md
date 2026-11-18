# Part 10 - Testing

## Strategy

| Level | What is tested | Files |
| --- | --- | --- |
| Unit: utilities | Every validation rule and the table formatter | `tests/test_validators.py`, `tests/test_formatters.py` |
| Unit: models | Abstraction (cannot instantiate), inheritance, polymorphism, encapsulation, business rule `cancel()` | `tests/test_person_models.py`, `tests/test_clinical_models.py` |
| Database | Tables, check constraints, unique constraints, foreign keys, rollback | `tests/test_database.py`, `tests/test_schema_relationships.py` |
| Service | Create, read, update, delete, search, duplicate rules, double booking, record linking, history, dashboard totals | `tests/test_patient_service.py`, `tests/test_doctor_service.py`, `tests/test_appointment_service.py`, `tests/test_medical_record_service.py`, `tests/test_dashboard_service.py` |
| Persistence | Data is still there after the database file is closed and reopened | `tests/test_persistence.py` |
| End-to-end | The real menus driven with scripted keyboard input | `tests/test_menus.py` |

All tests use Python's `unittest` and in-memory SQLite databases (`:memory:`) so they never touch
real data. `tests/helpers.py` builds valid sample objects.

## How to Run

```bash
python -m unittest discover -s tests -t . -v       # all tests, verbose
python -m unittest tests.test_validators           # one file
python -m unittest tests.test_menus.MenuTests.test_full_workflow_through_the_menus   # one test
```

## Results

```text
Ran 119 tests in about 0.1s

OK
```

| Test file | Tests |
| --- | --- |
| `test_validators.py` | 18 |
| `test_formatters.py` | 4 |
| `test_person_models.py` | 12 |
| `test_clinical_models.py` | 12 |
| `test_database.py` | 6 |
| `test_schema_relationships.py` | 5 |
| `test_patient_service.py` | 11 |
| `test_doctor_service.py` | 6 |
| `test_appointment_service.py` | 16 |
| `test_medical_record_service.py` | 15 |
| `test_dashboard_service.py` | 3 |
| `test_persistence.py` | 1 |
| `test_menus.py` | 10 |
| **Total** | **119** |

The tests also passed at the end of each development step during the rehearsal of the Git plan
(22, 34, 40, 57, 52, 85, 108, 119, 119 tests), so every merge into `main` left a working program.

## Requirement-to-Test Traceability

| Requirement | Test evidence |
| --- | --- |
| Register / search / update / delete / view patient | `test_patient_service.py`, `test_menus.py::test_search_update_and_delete_patient` |
| Register / search / update / delete / view doctor | `test_doctor_service.py`, `test_menus.py::test_doctor_search_update_view_delete` |
| Create / update / cancel / view appointments | `test_appointment_service.py`, `test_menus.py::test_appointment_update_cancel_and_view_filters` |
| Create / update medical record, view history | `test_medical_record_service.py`, `test_menus.py::test_medical_record_update_and_view_one` |
| Dashboard totals | `test_dashboard_service.py`, `test_menus.py::test_full_workflow_through_the_menus` |
| Data persistence | `test_persistence.py` |
| Encapsulation | `test_person_models.py::EncapsulationTests`, `test_clinical_models.py` |
| Inheritance | `test_person_models.py::InheritanceTests` |
| Polymorphism | `test_person_models.py::PolymorphismTests` |
| Abstraction | `test_person_models.py::AbstractionTests`, `test_patient_service.py::test_service_extends_abstract_base` |

## Important Edge Cases Covered

- Blank required answers are asked again; invalid dates, times, National IDs and phone numbers are rejected with a message.
- Duplicate National ID (patients and doctors) and duplicate licence number are rejected.
- A doctor cannot be booked twice for the same date and time; a cancelled slot becomes free again.
- Cancelling twice, or cancelling a completed appointment, is rejected.
- A medical record cannot be linked to a cancelled appointment or to another patient's appointment.
- Deleting a patient removes their appointments and records; deleting a doctor who still has appointments is refused.
- Deleting an appointment keeps the medical record (the link is set to empty).
- Unknown IDs produce `No patient found with ID 99.` style messages, never a crash.

## Manual Test: Real Console Session

The session below was produced by the program itself (answers shown after each prompt).

```text
Doctor Management
=================
  1. Register doctor
  ...
Choose an option: 1
...
Doctor registered with ID 1.

Patient registered with ID 1.        (phone typed as "077 123 4567" is stored as 0771234567)

Search by name, National ID or phone: moyo
ID | Name        | National ID    | Age | Gender | Phone      | Province
---+-------------+----------------+-----+--------+------------+---------
1  | Tendai Moyo | 63-123456-A-42 | 36  | Female | 0771234567 | Harare

Appointment created with ID 1.
Error: Doctor 1 already has appointment #1 on 2026-12-01 at 09:30.     (double booking refused)

Medical record created with ID 1.
Medical history for patient 1: 1 record(s)
ID | Visit      | Doctor          | Diagnosis    | Treatment                    | Prescription
---+------------+-----------------+--------------+------------------------------+---------------------
1  | 2026-12-01 | Farai Chikwanha | Hypertension | Lifestyle changes and mon... | Amlodipine 5mg daily

EHR Dashboard
=============
Total patients        : 1
Total doctors         : 1
Total appointments    : 1
Total medical records : 1

Appointments by status:
  Scheduled : 0
  Completed : 1
  Cancelled : 0
```

(The age column depends on today's date. The appointment shows as Completed because linking the
medical record to a scheduled appointment completes it.)

Persistence was also checked by hand: a doctor was registered, the program was closed, started
again, and the dashboard still reported `Total doctors : 1`.
