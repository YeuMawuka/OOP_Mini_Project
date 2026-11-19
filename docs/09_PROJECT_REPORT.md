# Part 9 - Project Report

---

## 1. Cover Page

**University of Zimbabwe**
**MSc Medical Analytics and Informatics**

**Module:** Object-Oriented Programming in Python
**Assessment:** OOP Mini Project 2026 (Group 2)

# Electronic Health Record (EHR) Management System

**A Python and SQLite application developed with Git and GitHub**

| | |
| --- | --- |
| **Group members** | Nicodimus (steps 1, 2, 3, 6, 7, 8, 9) and Yeukai (steps 4, 5, 10) |
| **Submission date** | 20 November 2026 |
| **GitHub repository** | `https://github.com/yeumawuka-stack/OOP_Mini_Project` (private; the lecturer is added as a collaborator) |
| **Release** | `v1.0.0` |

---

## 2. Abstract

This report describes the design, implementation and testing of an Electronic Health Record (EHR)
Management System built for a Zimbabwean clinic as the Object-Oriented Programming mini project of
the MSc in Medical Analytics and Informatics. The system is a menu-driven Python 3 application that
stores data in SQLite through Python's `sqlite3` module and uses no third-party packages. It lets
staff register, search, update, delete and view patients and doctors; create, update, cancel and
view appointments; create and update medical records and read a patient's medical history; and see
a dashboard of totals. The code is organised in five layers (user interface, services, models,
database and utilities) and demonstrates encapsulation through private attributes with validating
properties, inheritance through a `BaseEntity` > `Person` > `Patient`/`Doctor` hierarchy, polymorphism through
overridden methods, and abstraction through abstract base classes created with the `abc` module.
The program is verified by 119 automated unit tests. The project was developed by two students
using ten Git feature branches, ten pull requests with cross-reviews, merge commits, and one real
merge conflict that was resolved in `database/schema.py`.

## 3. Introduction

Health records are the foundation of safe care: a doctor who can see a patient's earlier diagnoses,
treatments and prescriptions makes better decisions. Biomedical informatics studies how such data
are captured, stored and used. This project applies object-oriented programming (OOP) to a small
but realistic EHR: patients, doctors, appointments and medical records are modelled as classes,
validated when they are created, and saved permanently in a relational database.

The project had two aims. The technical aim was a working EHR program that follows OOP principles.
The professional aim was to work like a real software team: sharing code on GitHub, using branches
and pull requests, reviewing each other's work, merging, and resolving a merge conflict.

## 4. Background

**Electronic Health Records.** An EHR is a digital version of a patient's clinical history. Typical
elements are demographics, allergies, diagnoses, treatments, prescriptions and visit dates. Digital
records are quicker to search, easier to back up and allow summary statistics, but they must protect
privacy. This system keeps its database in a local file excluded from version control so real patient
data is never uploaded to GitHub.

**Local context.** The system uses Zimbabwean conventions: National ID numbers such as
`63-123456-A-42`, phone numbers beginning `+263` or `0`, the ten provinces of Zimbabwe, and
practitioner licence numbers of the form `MDPCZ-10234`.

**OOP.** Encapsulation hides data behind controlled access; inheritance lets a child class reuse and
extend a parent; polymorphism lets different classes answer the same call in their own way;
abstraction defines what a class must do without saying how (Meyer, 1997; Gamma et al., 1994).

**SQLite.** SQLite is a serverless relational database stored in one file. Python includes it in the
standard library as `sqlite3`, so no installation is needed. It supports primary keys, foreign keys
(when enabled with `PRAGMA foreign_keys = ON`), unique and check constraints (Hipp, n.d.).

**Git and GitHub.** Git records every change as a commit and allows parallel work on branches. GitHub
hosts the repository and adds pull requests, reviews and branch protection (Chacon and Straub, 2014).

## 5. Problem Statement

Clinics that rely on paper cards or loose spreadsheets cannot search records quickly, cannot see a
patient's history at the point of care, double-book doctors, store inconsistent data, and cannot
produce simple totals. A small, reliable, locally stored EHR with validation and persistent storage
is needed, together with a development process that proves the work was shared fairly by the team.

## 6. Objectives

1. Build an EHR in Python 3 using only the standard library and SQLite.
2. Provide patient, doctor, appointment and medical record management with a dashboard.
3. Keep data permanently between program runs.
4. Demonstrate encapsulation, inheritance, polymorphism and abstraction clearly.
5. Validate input so the database contains consistent data.
6. Test the system with automated tests.
7. Use Git and GitHub with branching, pull requests, code review, merging and conflict resolution, and show that both members contributed.

## 7. System Analysis

**Users:** receptionist (registers patients, books appointments), doctor (writes records, reads
history), administrator (manages doctors, deletes records), manager (reads the dashboard).

**Functional requirements:** FR1-FR15 in `docs/01_SYSTEM_DESIGN.md` cover registering, searching,
updating, deleting and viewing patients and doctors; creating, updating, cancelling and viewing
appointments; creating and updating medical records and viewing history; the dashboard; and
persistence.

**Non-functional requirements:** standard library only, data integrity, beginner-friendly menus,
friendly error handling, maintainability through layers, testability, privacy through `.gitignore`,
and portability across Windows, macOS and Linux.

**Business rules found during analysis:**

- A National ID may belong to only one patient (and one doctor); a licence number to only one doctor.
- A doctor cannot have two scheduled appointments at the same date and time.
- A cancelled appointment stays in the database as history but frees the time slot.
- A medical record may be linked to an appointment of the *same patient* that is not cancelled; linking completes the appointment.
- Deleting a patient also deletes their appointments and records; a doctor with appointments or records cannot be deleted.

**Use cases:** thirteen use cases (UC1-UC13) are tabulated in `docs/01_SYSTEM_DESIGN.md`.

## 8. System Design

**Layered architecture.**

| Layer | Package | Main classes |
| --- | --- | --- |
| User interface | `ui/` | `Console`, `Menu`, `MainMenu`, `PatientMenu`, `DoctorMenu`, `AppointmentMenu`, `MedicalRecordMenu` |
| Services | `services/` | `BaseService`, `PatientService`, `DoctorService`, `AppointmentService`, `MedicalRecordService`, `DashboardService` |
| Domain model | `models/` | `BaseEntity`, `Person`, `Patient`, `Doctor`, `Appointment`, `MedicalRecord` |
| Persistence | `database/` | `Database`, `SCHEMA_SQL` |
| Utilities | `utils/` | `Validators`, `TableFormatter`, `EHRError` and four child exceptions |

**Data flow.** The user types an answer; `Console.ask` validates it with `Validators`; the menu builds
an entity whose setters validate again; a service applies business rules and runs a parameterised SQL
statement through `Database`; rows come back as entities through `from_row`; the menu prints
`describe()` text or a table. Any `EHRError` is caught in `Menu.run` and shown as `Error: ...`.

**Class relationships.** `BaseEntity` is the root of the entity classes; `Person` extends it and is the
parent of `Patient` and `Doctor`; `Appointment` and `MedicalRecord` extend `BaseEntity` directly.
`BaseService` is the parent of the four services, each of which uses one `Database`.
`DashboardService` is composed of the four services. `Menu` is the parent of the five menus. The
diagram is in `docs/01_SYSTEM_DESIGN.md` section 8.

**Design decisions.** The `services/` layer keeps SQL out of the entities, so entities stay simple
objects. The `Console` accepts replaceable input and output functions, which makes the whole menu
system testable without a keyboard. IDs are stored as foreign keys rather than object references,
keeping rows and objects loosely coupled.

## 9. OOP Concepts Applied

(Full table with every class, method and file: `docs/03_OOP_MAPPING.md`.)

**Encapsulation.** In `models/person.py` the fields `__first_name`, `__last_name`, `__national_id`,
`__date_of_birth`, `__gender`, `__phone` and `__email` are private. They are read through properties
and written through setters that call `Validators`, so `patient.phone = "bad"` raises
`ValidationError`. `BaseEntity` hides `__id`; `Appointment` hides its status and exposes `cancel()`
which enforces the cancellation rules; `Database` hides its `sqlite3` connection; `Console` hides its
input/output functions.

**Inheritance.** `BaseEntity` > `Person` > `Patient` and `Doctor` is three levels deep: `Patient` and
`Doctor` reuse names, National ID, dates, phone, `full_name` and `age` from `Person` through
`super().__init__`. `BaseService` supplies `get_by_id`, `list_all`, `count` and `delete` to all four
services; `Menu` supplies the `run()` loop to all five menus.

**Polymorphism.** `describe()` is overridden in `Patient`, `Doctor`, `Appointment` and
`MedicalRecord`; `get_role()` returns "Patient" or "Doctor"; `to_dict()` is extended by `Patient` and
`Doctor`; `create()`, `update()` and `search()` are overridden by each service (the appointment
service checks for double booking, the record service links appointments, and so on); each menu
overrides `title` and `options()`. The shared call `print(entity)` uses `BaseEntity.__str__`, which
calls the overridden `describe()` of the actual object.

**Abstraction.** `BaseEntity`, `Person`, `BaseService` and `Menu` derive from `abc.ABC` and declare
`@abstractmethod` members, so they cannot be instantiated (`tests/test_person_models.py` proves it)
and every child must implement the contract.

## 10. Database Design

Four tables (`patients`, `doctors`, `appointments`, `medical_records`) with `INTEGER PRIMARY KEY
AUTOINCREMENT` keys. `appointments` references `patients` (`ON DELETE CASCADE`) and `doctors`
(`ON DELETE RESTRICT`). `medical_records` references `patients` (`CASCADE`), `doctors` (`RESTRICT`)
and, optionally, `appointments` (`SET NULL`). `UNIQUE` constraints protect National IDs and licence
numbers; `CHECK` constraints restrict gender, province, blood group and appointment status; five
indexes speed up searches, the double-booking check and history queries.

Relationships: one patient has many appointments and many records; one doctor has many appointments
and many records; an appointment has at most one resulting record link. Delete rules protect clinical
data: removing an appointment never deletes the record written during it. The complete schema, a
relationship diagram and an explanation of each rule are in `docs/04_DATABASE_DESIGN.md` and
`database/schema.py`.

## 11. GitHub Collaboration Process

**Roles.** Nicodimus completed steps 1, 2, 3, 6, 7, 8 and 9 (project set-up, utilities, person
models, appointment and record models, appointment service, record and dashboard services, console
menus). Yeukai completed steps 4, 5 and 10 (database layer, patient and doctor services, final
documentation and release). Each student also reviewed the other's pull requests.

**Workflow.** `main` was kept clean by team agreement (GitHub branch protection is not offered for
private repositories on a free plan): no direct pushes, and no merge before the other student's
review. Each step used a branch `feature/NN-name`, small commits with imperative messages, a pull request using a common
description template, a review by the other student, and a merge commit. Branches were kept on GitHub
after merging so they remain visible. The ten steps, the exact Git commands, commit messages, pull
request titles and reviewers are in `docs/05_GITHUB_COLLABORATION_PLAN.md`; each pull request is
described in `docs/06_PULL_REQUEST_STRATEGY.md`.

**Code review.** Every pull request was assigned to the other student as reviewer, using a shared
checklist (docstrings, private attributes, abstract methods, parameterised SQL, tests, commit
quality). Reviews and approvals are visible on the Conversation tab of each pull request.

**Merge conflict.** Yeukai's step 5 and Nicodimus's step 7 both added text at the end of
`SCHEMA_SQL` in `database/schema.py` (search indexes versus the `appointments` table). After PR #5
was merged, GitHub reported a conflict on PR #7 and Git reported it again when Nicodimus ran
`git merge main`. He kept both blocks, removed the markers, committed the merge and pushed; the
conflict notice then disappeared and Yeukai reviewed the result. The details and real Git output are
in `docs/07_MERGE_CONFLICT_SCENARIO.md`.

**Proof of contribution.** The repository history shows commits by both students (Nicodimus authored
pull requests #1, #2, #3, #6, #7, #8 and #9; Yeukai authored #4, #5 and #10), each student reviewing
the other's work, the merge commits, the resolved conflict in PR #7 and the release tag `v1.0.0`.
Where to find each piece of evidence on GitHub is listed in `docs/08_EVIDENCE_OF_COLLABORATION.md`.

## 12. Implementation

**Technology.** Python 3 (tested on 3.13) with only `sqlite3`, `abc`, `re`, `datetime`, `os`,
`unittest` and `tempfile`. About 2,050 lines of source and 1,130 lines of tests, in 25 source files
and 15 test files.

**Utilities (`utils/`).** `Validators` holds every rule: names (letters, spaces, hyphens,
apostrophes), National ID (normalised to `63-123456-A-42`), phone (`+263` or `0` followed by nine digits,
spaces and hyphens ignored), e-mail, real calendar dates, date of birth (not in the future), 24-hour
times, case-insensitive choices and positive IDs. `TableFormatter` builds aligned tables. Four
exceptions inherit from `EHRError`.

**Models (`models/`).** Each entity validates every assignment. `from_row` rebuilds an entity from a
database row. `Appointment.cancel()` refuses to cancel an appointment twice or after completion.

**Database (`database/`).** `Database.__init__` creates the `data/` folder and file, opens the
connection with `sqlite3.Row` rows, enables foreign keys and runs the schema script. `execute()`
commits, or rolls back and re-raises on error. The default file is `data/ehr.db`.

**Services (`services/`).** `BaseService._insert` and `_update_row` build parameterised SQL from the
column list each service declares, which removes duplicated SQL code. `PatientService` and
`DoctorService` enforce unique identifiers. `AppointmentService._ensure_doctor_free` prevents double
booking. `MedicalRecordService._check_links` validates the patient, doctor and appointment and
completes a linked scheduled appointment. `DashboardService.render()` prints totals and the number of
appointments by status.

**User interface (`ui/`, `main.py`).** `Menu.run()` prints numbered options, reads a choice and
calls the handler inside `try/except EHRError`. `Console.ask()` repeats a question until the answer
is valid and supports defaults shown in brackets, which the update screens use so that pressing
Enter keeps the current value. `main.py` creates the services and menus in `build_application()` and
closes the database in a `finally` block; Ctrl+C or end of input ends the session politely.

**How to run.** `python main.py`; tests: `python -m unittest discover -s tests -t . -v`.

## 13. Testing

119 `unittest` tests cover the validators and formatter (22), person models (12), clinical models
(12), database and schema constraints (11), the four services and dashboard (51), persistence (1) and
end-to-end menu sessions (10). Tests use in-memory databases so real data is never touched.
`test_persistence.py` writes data to a temporary file, closes the database, reopens it and verifies the
data is still there. `test_menus.py` types complete sessions into the real menus using scripted
input. The result is:

```text
Ran 119 tests in about 0.1s

OK
```

The tests also passed at the end of every development step. Details and a requirement-to-test
traceability table are in `docs/10_TESTING.md`.

## 14. Results

A manual session on the finished program produced the following output (abridged from
`docs/10_TESTING.md`):

```text
Doctor registered with ID 1.
Patient registered with ID 1.
ID | Name        | National ID    | Age | Gender | Phone      | Province
1  | Tendai Moyo | 63-123456-A-42 | 36  | Female | 0771234567 | Harare
Appointment created with ID 1.
Error: Doctor 1 already has appointment #1 on 2026-12-01 at 09:30.
Medical record created with ID 1.
Medical history for patient 1: 1 record(s)
Total patients        : 1
Total doctors         : 1
Total appointments    : 1
Total medical records : 1
  Completed : 1
```

Every functional requirement FR1-FR15 is available from the menus. Data survived closing and reopening
the program. Invalid input was rejected with a message and no crash. The double-booking rule, the
duplicate National ID rule, the appointment-linking rules and the delete rules all behaved as designed.

## 15. Challenges

- **Foreign keys are off by default in SQLite.** Relationships were silently ignored until `PRAGMA foreign_keys = ON` was added to every connection; tests in `test_schema_relationships.py` now guard it.
- **Choosing delete behaviour.** Deleting a patient must not leave orphan rows, but clinical notes must survive when an appointment is removed and a doctor must not disappear while records name them. This led to the `CASCADE`, `RESTRICT` and `SET NULL` choices, and to the warning that the delete-patient prompt shows about appointments and records.
- **Keeping validation in one place.** The same National ID or phone rule was needed in the menus, the models and the tests; moving all rules to the `Validators` class removed the duplication.
- **Testing a menu-driven program.** `input()` blocks automated tests. Wrapping input and output in the `Console` class made it possible to feed scripted answers.
- **Working in parallel on one file.** Both students changed `database/schema.py`, producing the merge conflict. Reading both versions before editing and keeping both blocks solved it; the full test suite then passed after all merges.
- **Learning Git as beginners.** Small commits, a fixed command routine, the agreed no-direct-push rule and cross-reviews kept the history readable and prevented mistakes on `main`.

## 16. Conclusion

The project delivers a complete, tested EHR Management System that meets every functional
requirement, stores data permanently in SQLite, uses only the Python standard library, and shows
encapsulation, inheritance, polymorphism and abstraction in meaningful classes. The development
followed real team practice: ten branches, ten reviewed pull requests, merge commits, a resolved merge
conflict and a tagged release, with commit history showing contributions from both students.

Possible future work: a graphical or web interface; user accounts and roles with audit logs;
encryption of the database and compliance with Zimbabwe's Cyber and Data Protection Act (2021);
standard coding systems such as ICD-10; export to PDF; and a continuous-integration workflow on
GitHub that runs the tests on every pull request.

## 17. References

Chacon, S. and Straub, B. (2014) *Pro Git*. 2nd edn. New York: Apress. Available at: https://git-scm.com/book.

GitHub (n.d.) *GitHub Docs: About pull requests; About protected branches; Resolving a merge conflict using the command line*. Available at: https://docs.github.com.

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. Reading, MA: Addison-Wesley.

Hipp, D. R. (n.d.) *SQLite documentation*, including *Foreign Key Support*. Available at: https://www.sqlite.org/docs.html.

Martin, R. C. (2008) *Clean Code: A Handbook of Agile Software Craftsmanship*. Upper Saddle River, NJ: Prentice Hall.

Meyer, B. (1997) *Object-Oriented Software Construction*. 2nd edn. Upper Saddle River, NJ: Prentice Hall.

Python Software Foundation (n.d.) *Python 3 documentation: abc, sqlite3, unittest, datetime and re modules*. Available at: https://docs.python.org/3/.

Republic of Zimbabwe (2021) *Cyber and Data Protection Act*. Harare: Government Printer.
