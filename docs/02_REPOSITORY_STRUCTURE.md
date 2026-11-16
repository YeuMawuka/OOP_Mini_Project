# Part 2 - Repository Structure

```text
EHR-System/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── schema.py
├── models/
│   ├── __init__.py
│   ├── base_entity.py
│   ├── person.py
│   ├── patient.py
│   ├── doctor.py
│   ├── appointment.py
│   └── medical_record.py
├── services/
│   ├── __init__.py
│   ├── base_service.py
│   ├── patient_service.py
│   ├── doctor_service.py
│   ├── appointment_service.py
│   ├── medical_record_service.py
│   └── dashboard_service.py
├── ui/
│   ├── __init__.py
│   ├── console.py
│   └── menus.py
├── utils/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── validators.py
│   └── formatters.py
├── tests/
│   ├── __init__.py
│   ├── helpers.py
│   ├── test_validators.py
│   ├── test_formatters.py
│   ├── test_person_models.py
│   ├── test_clinical_models.py
│   ├── test_database.py
│   ├── test_schema_relationships.py
│   ├── test_patient_service.py
│   ├── test_doctor_service.py
│   ├── test_appointment_service.py
│   ├── test_medical_record_service.py
│   ├── test_dashboard_service.py
│   ├── test_persistence.py
│   └── test_menus.py
└── docs/
    ├── 01_SYSTEM_DESIGN.md
    ├── 02_REPOSITORY_STRUCTURE.md
    ├── 03_OOP_MAPPING.md
    ├── 04_DATABASE_DESIGN.md
    ├── 05_GITHUB_COLLABORATION_PLAN.md
    ├── 06_PULL_REQUEST_STRATEGY.md
    ├── 07_MERGE_CONFLICT_SCENARIO.md
    ├── 08_EVIDENCE_OF_COLLABORATION.md
    ├── 09_PROJECT_REPORT.md
    ├── 10_TESTING.md
    └── 12_COMPLIANCE_CHECK.md
```

The `data/` folder (holding `ehr.db`) is created when the program first runs and is ignored by Git.
Every folder that contains Python files has an `__init__.py` so Python treats it as a package.

## Purpose of Every File

### Root

| File | Purpose |
| --- | --- |
| `main.py` | Entry point. `build_application()` creates the database, services and menus and returns the main menu; `main()` runs it and closes the database on exit. |
| `README.md` | Project overview, features, installation, usage, database setup and contributors. |
| `requirements.txt` | States that no third-party packages are needed and which Python version is required. |
| `.gitignore` | Keeps bytecode, virtual environments, the SQLite database and editor files out of Git. |

### `database/`

| File | Purpose |
| --- | --- |
| `__init__.py` | Marks the folder as a package. |
| `connection.py` | `Database` class: opens SQLite, enables foreign keys, creates tables, offers `execute`, `fetch_one`, `fetch_all`, `scalar`, `close`. |
| `schema.py` | `SCHEMA_SQL`: all `CREATE TABLE` and `CREATE INDEX` statements. |

### `models/`

| File | Purpose |
| --- | --- |
| `__init__.py` | Marks the folder as a package. |
| `base_entity.py` | Abstract `BaseEntity` with private `id`, abstract `to_dict()` and `describe()`. |
| `person.py` | Abstract `Person` with shared validated personal data, `full_name`, `age`, abstract `get_role()`. |
| `patient.py` | `Patient(Person)` with address, province, blood group, allergies and emergency contact. |
| `doctor.py` | `Doctor(Person)` with specialization, licence number and department. |
| `appointment.py` | `Appointment(BaseEntity)` with date, time, reason, status and the `cancel()` rule. |
| `medical_record.py` | `MedicalRecord(BaseEntity)` with diagnosis, treatment, prescription and notes. |

### `services/`

| File | Purpose |
| --- | --- |
| `__init__.py` | Marks the folder as a package. |
| `base_service.py` | Abstract `BaseService`: shared `get_by_id`, `list_all`, `count`, `delete` and SQL helpers. |
| `patient_service.py` | `PatientService`: unique National ID, patient search. |
| `doctor_service.py` | `DoctorService`: unique National ID and licence, doctor search. |
| `appointment_service.py` | `AppointmentService`: existence checks, double-booking rule, cancel, filtered listing, status counts. |
| `medical_record_service.py` | `MedicalRecordService`: link checks, auto-complete appointment, patient history. |
| `dashboard_service.py` | `DashboardService`: totals for the dashboard. |

### `ui/`

| File | Purpose |
| --- | --- |
| `__init__.py` | Marks the folder as a package. |
| `console.py` | `Console`: validated prompts (`ask`, `ask_id`, `ask_choice`, `confirm`) with replaceable input/output for tests. |
| `menus.py` | Abstract `Menu` plus `MainMenu`, `PatientMenu`, `DoctorMenu`, `AppointmentMenu`, `MedicalRecordMenu`. |

### `utils/`

| File | Purpose |
| --- | --- |
| `__init__.py` | Marks the folder as a package. |
| `exceptions.py` | `EHRError` and its four child exceptions. |
| `validators.py` | `Validators`: all input rules (names, National ID, phone, email, dates, times, choices, IDs, licence). |
| `formatters.py` | `TableFormatter`: headings and aligned text tables. |

### `tests/`

| File | Purpose |
| --- | --- |
| `__init__.py` | Marks the folder as a package so `unittest discover` finds the tests. |
| `helpers.py` | Builders for valid sample patients, doctors, appointments and records. |
| `test_validators.py` | 18 tests of every validation rule. |
| `test_formatters.py` | 4 tests of the table formatter. |
| `test_person_models.py` | 12 tests of abstraction, inheritance, polymorphism and encapsulation in `Person`, `Patient`, `Doctor`. |
| `test_clinical_models.py` | 12 tests of `Appointment` and `MedicalRecord`. |
| `test_database.py` | 6 tests of the connection wrapper and people tables. |
| `test_schema_relationships.py` | 5 tests of foreign keys and check constraints. |
| `test_patient_service.py` | 11 tests of patient create, search, update, delete. |
| `test_doctor_service.py` | 6 tests of doctor rules. |
| `test_appointment_service.py` | 16 tests of scheduling rules, cancel and filters. |
| `test_medical_record_service.py` | 15 tests of records, links and history. |
| `test_dashboard_service.py` | 3 tests of dashboard totals. |
| `test_persistence.py` | 1 test proving data survives closing and reopening the database file. |
| `test_menus.py` | 10 end-to-end tests that type into the menus with scripted input. |

### `docs/`

| File | Purpose |
| --- | --- |
| `01_SYSTEM_DESIGN.md` | System overview, requirements, use cases, data flow, class relationships. |
| `02_REPOSITORY_STRUCTURE.md` | This file. |
| `03_OOP_MAPPING.md` | Exact classes, methods and files for each OOP principle. |
| `04_DATABASE_DESIGN.md` | Schema, keys, constraints and relationships. |
| `05_GITHUB_COLLABORATION_PLAN.md` | The 10-step plan with branches, commands, commits and reviewers. |
| `06_PULL_REQUEST_STRATEGY.md` | All 10 pull requests. |
| `07_MERGE_CONFLICT_SCENARIO.md` | The merge conflict in `database/schema.py` and how it is resolved. |
| `08_EVIDENCE_OF_COLLABORATION.md` | What the lecturer sees on GitHub. |
| `09_PROJECT_REPORT.md` | The submission report. |
| `10_TESTING.md` | Test strategy, how to run, results. |
| `12_COMPLIANCE_CHECK.md` | Requirement-by-requirement compliance table. |
