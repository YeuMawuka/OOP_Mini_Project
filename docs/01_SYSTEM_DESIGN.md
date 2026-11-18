# Part 1 - System Design

## 1. System Overview

The EHR Management System is a console (menu-driven) application written in Python 3 that stores
patients, doctors, appointments and medical records in a SQLite database. It follows a layered
design so that each layer has one job:

| Layer | Package | Responsibility |
| --- | --- | --- |
| Presentation | `ui/` | Shows menus, reads typed answers, prints tables and messages |
| Business logic | `services/` | Applies hospital rules (unique National ID, no double booking, linking records to appointments) and talks to SQLite |
| Domain model | `models/` | Entity classes that validate and protect their own data |
| Persistence | `database/` | Opens the SQLite file and creates the tables |
| Utilities | `utils/` | Validation rules, text tables, custom exceptions |

A user starts `main.py`, chooses an option in a menu, the menu calls a service, the service uses
model objects and the `Database` class, and the result is printed back to the user.

## 2. Problem Statement

Many clinics in Zimbabwe still keep patient information on paper cards or in loose spreadsheets.
Paper files are slow to search, easy to lose, impossible to analyse and cannot show a doctor a
patient's earlier visits on the spot. Appointments are double-booked, patient details are spelled
differently on different forms, and nobody can quickly say how many patients, doctors or visits
the clinic handles. A small, reliable, locally stored electronic record system that checks the
data when it is typed and keeps it after the computer is switched off is needed.

## 3. Objectives

1. Build an EHR system in Python using only the standard library and SQLite.
2. Let staff register, search, update, delete and view patients and doctors.
3. Let staff create, update, cancel and view appointments without double-booking a doctor.
4. Let doctors create and update medical records and read a patient's complete history.
5. Show a dashboard with the total patients, doctors, appointments and medical records.
6. Keep all data after the program closes and reopens.
7. Demonstrate encapsulation, inheritance, polymorphism and abstraction with meaningful classes.
8. Develop the project as a team using Git branches, pull requests, code reviews, merging and
   merge-conflict resolution on GitHub, with clear evidence that both members contributed.

## 4. Functional Requirements

| ID | Requirement |
| --- | --- |
| FR1 | Register a patient with name, National ID, date of birth, gender, phone, email, address, province, blood group, allergies and emergency contact. |
| FR2 | Search patients by name, National ID or phone number. |
| FR3 | Update any patient field; pressing Enter keeps the current value. |
| FR4 | Delete a patient after confirmation (their appointments and medical records are deleted with them). |
| FR5 | View one patient in full, and list all patients. |
| FR6 | Register, search, update, delete and view doctors (name, National ID, specialization, licence number, department). |
| FR7 | Create an appointment for an existing patient and doctor. |
| FR8 | Update an appointment (doctor, date, time, reason, status). |
| FR9 | Cancel an appointment; the row is kept for history. |
| FR10 | View appointments: all, by patient, by doctor or by status. |
| FR11 | Create a medical record (diagnosis, treatment, prescription, notes), optionally linked to an appointment. |
| FR12 | View a patient's medical history, newest visit first. |
| FR13 | Update a medical record. |
| FR14 | Show a dashboard with total patients, doctors, appointments, medical records and appointments by status. |
| FR15 | Store all data in SQLite so it is available after restart. |

## 5. Non-Functional Requirements

| ID | Requirement | How it is met |
| --- | --- | --- |
| NFR1 | Uses only Python 3 standard library | No third-party imports anywhere; `requirements.txt` says so |
| NFR2 | Data integrity | `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL` and `CHECK` constraints plus validation in the classes |
| NFR3 | Usability for beginners | Numbered menus, prompts with examples, defaults in brackets, plain error messages |
| NFR4 | Reliability | Custom exceptions are caught by the menu loop, so the program does not crash on bad input |
| NFR5 | Maintainability | Layered packages, one class per file, docstrings, no repeated validation code |
| NFR6 | Testability | 119 automated `unittest` tests; the console accepts scripted input |
| NFR7 | Privacy | The database file is excluded from Git by `.gitignore` |
| NFR8 | Portability | Runs on Windows, macOS and Linux with Python 3.9 or newer |

## 6. Use Cases

| ID | Use case | Actor | Main flow | Alternative / error flow |
| --- | --- | --- | --- | --- |
| UC1 | Register patient | Receptionist | Patient menu, Register, answer prompts, system stores patient and shows the new ID | Invalid value: prompt repeats. Duplicate National ID: error message |
| UC2 | Search patient | Receptionist, Doctor | Enter a keyword, system lists matching patients | No match: "(no records found)" |
| UC3 | Update patient | Receptionist | Enter ID, change fields, system saves | Unknown ID: error. National ID used by someone else: error |
| UC4 | Delete patient | Administrator | Enter ID, confirm, system deletes patient and dependent rows | Answer "n": nothing deleted |
| UC5 | Manage doctors | Administrator | Same flows as UC1 to UC4 for doctors | Doctor with appointments or records cannot be deleted |
| UC6 | Create appointment | Receptionist | Enter patient ID, doctor ID, date, time, reason | Doctor already booked at that time: error |
| UC7 | Update appointment | Receptionist | Enter ID, change doctor, date, time, reason or status | New slot taken: error |
| UC8 | Cancel appointment | Receptionist | Enter ID, confirm, status becomes Cancelled | Already cancelled or completed: error |
| UC9 | View appointments | Receptionist, Doctor | Choose a filter, system lists appointments with patient and doctor names | None found: message |
| UC10 | Create medical record | Doctor | Enter patient, doctor, optional appointment, visit details | Appointment of another patient or cancelled: error. Linked scheduled appointment becomes Completed |
| UC11 | View medical history | Doctor | Enter patient ID, system lists all visits | Unknown patient: error |
| UC12 | Update medical record | Doctor | Enter record ID, change fields | Unknown ID: error |
| UC13 | View dashboard | Manager | Choose Dashboard, system prints totals | Empty system shows zeros |

## 7. Data Flow Description

1. **Input:** the user types an answer at a prompt (`ui/console.py`).
2. **Validation:** `Console.ask` calls a `Validators` method; invalid text is rejected and asked again.
3. **Object creation:** the menu builds an entity (for example `Patient`). Its property setters validate every field again, so an invalid object can never exist.
4. **Business rules:** the menu passes the entity to a service (`PatientService.create`). The service checks rules such as "National ID not already used".
5. **Persistence:** the service builds an SQL statement with `?` placeholders and runs it through `Database.execute`, which commits (or rolls back on error).
6. **Retrieval:** `get_by_id`, `search`, `list_all` and `get_history` run `SELECT` statements; each row becomes an entity again through `from_row`.
7. **Output:** the menu prints `describe()` text or a table made by `TableFormatter`.
8. **Errors:** any `EHRError` raised below is caught in `Menu.run` and printed as `Error: ...`.

```text
User -> Console -> Validators -> Menu -> Model (validates) -> Service (rules) -> Database -> SQLite file
User <- Console <- Menu <- TableFormatter / describe() <- Model <- Service <- Database <-+
```

## 8. Class Relationships

```text
BaseEntity (abstract)                     BaseService (abstract)
 |  - id (private, property)               |  - _db : Database
 |  + to_dict()  (abstract)                |  + create / update / search (abstract)
 |  + describe() (abstract)                |  + get_by_id, list_all, count, delete
 |                                         |
 +-- Person (abstract)                     +-- PatientService
 |    |  + get_role() (abstract)           +-- DoctorService
 |    |                                    +-- AppointmentService
 |    +-- Patient                          +-- MedicalRecordService
 |    +-- Doctor
 +-- Appointment                          DashboardService  (uses all four services)
 +-- MedicalRecord

Menu (abstract)
 +-- MainMenu  (uses the four menus and DashboardService)
 +-- PatientMenu       -> PatientService
 +-- DoctorMenu        -> DoctorService
 +-- AppointmentMenu   -> AppointmentService
 +-- MedicalRecordMenu -> MedicalRecordService

Database  (used by every service)      Console (used by every menu)
Validators, TableFormatter  (static utility classes)
EHRError -> ValidationError, NotFoundError, DuplicateError, BusinessRuleError
```

| Relationship | Type | Meaning |
| --- | --- | --- |
| Patient, Doctor to Person | Inheritance | A patient *is a* person |
| Person, Appointment, MedicalRecord to BaseEntity | Inheritance | All entities share ID handling and the `describe`/`to_dict` contract |
| Each service to BaseService | Inheritance | All services share `get_by_id`, `list_all`, `count`, `delete` |
| Each menu to Menu | Inheritance | All menus share the `run()` loop |
| Service to Database | Association | A service *uses* a database connection |
| DashboardService to the four services | Composition/aggregation | The dashboard *has* the services it summarises |
| Appointment to Patient and Doctor | Association by ID | Stored as foreign keys |
| MedicalRecord to Patient, Doctor, Appointment | Association by ID | Stored as foreign keys |

## 9. OOP Design Explanation

- **Encapsulation:** entity fields are private (`self.__first_name`) and reached only through properties whose setters validate. `Database` hides its `sqlite3` connection; `Console` hides its input/output functions; `DashboardService` hides the services it combines.
- **Inheritance:** `Person` is the parent of `Patient` and `Doctor`; `BaseEntity` is the parent of `Person`, `Appointment` and `MedicalRecord`; `BaseService` is the parent of all four services; `Menu` is the parent of all five menus.
- **Polymorphism:** `describe()`, `to_dict()` and `get_role()` are overridden in each entity; `create()`, `update()` and `search()` are overridden in each service; every menu overrides `title` and `options()` but is started by the same `run()`.
- **Abstraction:** `BaseEntity`, `Person`, `BaseService` and `Menu` use `abc.ABC` and `@abstractmethod`, so they cannot be instantiated and force children to implement the contract.

The exact classes, methods and files are listed in `docs/03_OOP_MAPPING.md`.
