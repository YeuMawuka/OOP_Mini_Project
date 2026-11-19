# Part 5 - GitHub Collaboration Plan

Team: **Nicodimus** (steps 1, 2, 3, 6, 7, 8 and 9) and **Yeukai** (steps 4, 5 and 10).
Every step uses its own branch, a pull request (PR), a review by the *other* student, and a merge into `main`.

| Item | Value |
| --- | --- |
| Repository | `https://github.com/yeumawuka-stack/OOP_Mini_Project` (Private) |
| Repository owner | Yeukai (`yeumawuka-stack`) |
| Collaborators | Nicodimus (`NicodimusTinashe`, Write access) and the lecturer |
| Default branch | `main` |
| Merge method | **Create a merge commit** for every PR, remote branches kept |
| Release | Tag `v1.0.0` |

The plan was rehearsed end to end in a practice repository before it was carried out. The tests pass
after every merge: 22 tests after step 2, 34 after step 3, 40 after step 4, 57 after step 5, 69 after
step 6, 85 after step 7, 108 after step 8 and 119 after step 9 (step 10 adds documents only).

## Who does what

| Step | Branch | Author | Reviewer | PR |
| --- | --- | --- | --- | --- |
| 1 Project set-up | `feature/01-project-setup` | Nicodimus | Yeukai | #1 |
| 2 Utilities | `feature/02-utilities` | Nicodimus | Yeukai | #2 |
| 3 Person models | `feature/03-person-models` | Nicodimus | Yeukai | #3 |
| 4 Database layer | `feature/04-database-layer` | Yeukai | Nicodimus | #4 |
| 5 Patient and doctor services | `feature/05-patient-doctor-services` | Yeukai | Nicodimus | #5 |
| 6 Appointment and record models | `feature/06-appointment-record-models` | Nicodimus | Yeukai | #6 |
| 7 Appointment service | `feature/07-appointment-service` | Nicodimus | Yeukai | #7 |
| 8 Record and dashboard services | `feature/08-record-and-dashboard-services` | Nicodimus | Yeukai | #8 |
| 9 Console menus | `feature/09-console-menus` | Nicodimus | Yeukai | #9 |
| 10 Final documents and release | `feature/10-final-docs-and-release` | Yeukai | Nicodimus | #10 |

Pull requests were opened in numerical order so that the numbers on GitHub match the step numbers.

## Step 0 - One-time setup

**Yeukai** (repository owner) created the private repository `OOP_Mini_Project` with a README
(commit "Initial commit") and added Nicodimus under **Settings > Collaborators** with Write access.
The lecturer is added the same way before submission.

GitHub does not offer branch protection rules for private repositories on a free plan, so the team
applied the same rules **by agreement**: nobody pushes directly to `main`; every step goes through a
pull request; a pull request is merged only after the other student has reviewed it; every merge uses
**Create a merge commit**; and no branch is deleted.

**Both students**, once per computer:

```bash
git config --global user.name  "Your Full Name"
git config --global user.email "the-email-used-on-github@example.com"
git clone https://github.com/yeumawuka-stack/OOP_Mini_Project.git
cd OOP_Mini_Project
```

The e-mail must be the one registered on the student's GitHub account, otherwise GitHub does not link
the commits to the profile.

### Routine used in every step

```bash
git switch main                       # go to main
git pull origin main                  # get everybody's latest work
git switch -c feature/NN-name         # create and move to the step branch
# ... create the files, then for each commit:
git add <files>
git commit -m "<message>"
git push -u origin feature/NN-name    # first push of the branch (later: git push)
# On GitHub: Compare & pull request, set the title, add the description, choose the reviewer, Create pull request
# Reviewer: Files changed > Review changes > Approve > Submit review
# Merge: Merge pull request > Create a merge commit > Confirm merge  (never "Delete branch")
git switch main
git pull origin main
```

Check your work before every push: `python -m unittest discover -s tests -t . -v`

---

## Step 1 - Project set-up (Nicodimus)

| Item | Detail |
| --- | --- |
| **Goal** | Create the project skeleton: ignore rules, requirements, README and the first two design documents. |
| **Branch** | `feature/01-project-setup` |
| **Files** | `.gitignore`, `requirements.txt`, `README.md`, `docs/01_SYSTEM_DESIGN.md`, `docs/02_REPOSITORY_STRUCTURE.md` |
| **Reviewer** | Yeukai |
| **PR** | #1 `Step 1: Project set-up, README and system design` |

The repository started with a file that had been saved as `,gitignore` (a comma instead of a dot). A
correct `.gitignore` was added and the misnamed file removed with `git rm ,gitignore`, in its own
commit, which is noted in the PR description.

```bash
git switch main && git pull origin main
git switch -c feature/01-project-setup
git add .gitignore requirements.txt
git commit -m "Add .gitignore and requirements.txt"
git add README.md
git commit -m "Add README with overview, installation and usage"
git add docs/01_SYSTEM_DESIGN.md docs/02_REPOSITORY_STRUCTURE.md
git commit -m "Add system design and repository structure documents"
git push -u origin feature/01-project-setup
```

**Merge:** Yeukai reviews and approves; Nicodimus merges with *Create a merge commit* (`Merge pull request #1 from yeumawuka-stack/feature/01-project-setup`).

---

## Step 2 - Utilities: exceptions, validators, formatter (Nicodimus)

| Item | Detail |
| --- | --- |
| **Goal** | Build the shared utility classes: exception hierarchy, `Validators`, `TableFormatter`, and their tests. |
| **Branch** | `feature/02-utilities` |
| **Files** | `utils/__init__.py`, `utils/exceptions.py`, `utils/validators.py`, `utils/formatters.py`, `tests/__init__.py`, `tests/test_validators.py`, `tests/test_formatters.py` |
| **Reviewer** | Yeukai |
| **PR** | #2 `Step 2: Utility classes (exceptions, validators, formatter)` |

```bash
git switch main && git pull origin main
git switch -c feature/02-utilities
git add utils/__init__.py utils/exceptions.py
git commit -m "Add custom exception hierarchy"
git add utils/validators.py
git commit -m "Add Validators utility class"
git add utils/formatters.py
git commit -m "Add TableFormatter utility class"
git add tests/__init__.py tests/test_validators.py tests/test_formatters.py
git commit -m "Add unit tests for validators and formatter"
git push -u origin feature/02-utilities
```

**Merge:** Yeukai approves; Nicodimus merges with *Create a merge commit* (`Merge pull request #2 ...`).

---

## Step 3 - Abstract base entity and Person models (Nicodimus)

| Item | Detail |
| --- | --- |
| **Goal** | Implement abstraction, inheritance, polymorphism and encapsulation in the domain model: `BaseEntity` > `Person` > `Patient`, `Doctor`. |
| **Branch** | `feature/03-person-models` |
| **Files** | `models/__init__.py`, `models/base_entity.py`, `models/person.py`, `models/patient.py`, `models/doctor.py`, `tests/helpers.py`, `tests/test_person_models.py` |
| **Reviewer** | Yeukai |
| **PR** | #3 `Step 3: Base Entity, Person, Patient and Doctor classes` |

```bash
git switch main && git pull origin main
git switch -c feature/03-person-models
git add models/__init__.py models/base_entity.py
git commit -m "Add abstract BaseEntity class"
git add models/person.py
git commit -m "Add abstract Person class with encapsulated fields"
git add models/patient.py models/doctor.py
git commit -m "Add Patient and Doctor classes inheriting from Person"
git add tests/helpers.py tests/test_person_models.py
git commit -m "Add test helpers and model tests"
git push -u origin feature/03-person-models
```

**Merge:** Yeukai approves; Nicodimus merges with *Create a merge commit* (`Merge pull request #3 ...`).

---

## Step 4 - Database layer and abstract service (Yeukai)

| Item | Detail |
| --- | --- |
| **Goal** | Add the SQLite connection class, the first part of the schema (patients and doctors tables), the abstract `BaseService`, the database design document and database tests. |
| **Branch** | `feature/04-database-layer` |
| **Files** | `database/__init__.py`, `database/connection.py`, `database/schema.py` (first version), `services/__init__.py`, `services/base_service.py`, `docs/04_DATABASE_DESIGN.md`, `tests/test_database.py` |
| **Reviewer** | Nicodimus |
| **PR** | #4 `Step 4: Database connection, schema and BaseService` |

```bash
git switch main && git pull origin main
git switch -c feature/04-database-layer
git add database/__init__.py database/connection.py database/schema.py
git commit -m "Add Database wrapper and patients and doctors tables"
git add services/__init__.py services/base_service.py
git commit -m "Add abstract BaseService class"
git add docs/04_DATABASE_DESIGN.md
git commit -m "Add database design document"
git add tests/test_database.py
git commit -m "Add database tests"
git push -u origin feature/04-database-layer
```

**Merge:** Yeukai merges with *Create a merge commit* (`Merge pull request #4 from yeumawuka-stack/feature/04-database-layer`).

---

## Step 5 - Patient and Doctor services (Yeukai)

| Item | Detail |
| --- | --- |
| **Goal** | Implement `PatientService` and `DoctorService` (create, update, search with unique-ID rules) and add search indexes to the schema. |
| **Branch** | `feature/05-patient-doctor-services` |
| **Files** | `services/patient_service.py`, `services/doctor_service.py`, `database/schema.py` (adds two indexes), `tests/test_patient_service.py`, `tests/test_doctor_service.py` |
| **Reviewer** | Nicodimus |
| **PR** | #5 `Step 5: PatientService and DoctorService` |

```bash
git switch main && git pull origin main
git switch -c feature/05-patient-doctor-services
git add services/patient_service.py
git commit -m "Add PatientService with unique National ID rule"
git add services/doctor_service.py
git commit -m "Add DoctorService with unique licence rule"
git add database/schema.py
git commit -m "Add search indexes for patients and doctors"
git add tests/test_patient_service.py tests/test_doctor_service.py
git commit -m "Add patient and doctor service tests"
git push -u origin feature/05-patient-doctor-services
```

**Merge:** PR #5 is left open until Nicodimus has opened PR #7 (this is what creates the realistic conflict). Nicodimus reviews and approves it and then merges it with *Create a merge commit* (`Merge pull request #5 from yeumawuka-stack/feature/05-patient-doctor-services`).

---

## Step 6 - Appointment and MedicalRecord models (Nicodimus)

| Item | Detail |
| --- | --- |
| **Goal** | Add the two remaining entity classes that inherit from `BaseEntity`, with validation and the `cancel()` business rule. |
| **Branch** | `feature/06-appointment-record-models` |
| **Files** | `models/appointment.py`, `models/medical_record.py`, `tests/test_clinical_models.py` |
| **Reviewer** | Yeukai |
| **PR** | #6 `Step 6: Appointment and MedicalRecord classes` |

```bash
git switch main && git pull origin main
git switch -c feature/06-appointment-record-models
git add models/appointment.py
git commit -m "Add Appointment class with cancel rule"
git add models/medical_record.py
git commit -m "Add MedicalRecord class"
git add tests/test_clinical_models.py
git commit -m "Add tests for Appointment and MedicalRecord"
git push -u origin feature/06-appointment-record-models
```

**Merge:** Yeukai approves and merges with *Create a merge commit* (`Merge pull request #6 ...`).

---

## Step 7 - Appointment service and the merge conflict (Nicodimus)

| Item | Detail |
| --- | --- |
| **Goal** | Implement `AppointmentService` (existence checks, double-booking rule, cancel, filtered listing) and add the `appointments` table. Resolve the merge conflict in `database/schema.py`. |
| **Branch** | `feature/07-appointment-service` |
| **Files** | `services/appointment_service.py`, `tests/test_appointment_service.py`, `database/schema.py` (adds the appointments table) |
| **Reviewer** | Yeukai |
| **PR** | #7 `Step 7: AppointmentService and appointments table` |

The branch was created and pushed with the service and its tests while Yeukai's PR #5 was still open.
Once Yeukai's step 4 was merged, Nicodimus brought `main` into the branch and added the table:

```bash
git switch -c feature/07-appointment-service
git add services/appointment_service.py
git commit -m "Add AppointmentService with double-booking rule"
git add tests/test_appointment_service.py
git commit -m "Add appointment service tests"
git push -u origin feature/07-appointment-service
# later, after step 4 is on main:
git switch main && git pull origin main
git switch feature/07-appointment-service
git merge main -m "Merge main into feature/07-appointment-service"
git add database/schema.py              # adds the appointments table
git commit -m "Add appointments table to the schema"
git push
# PR #7 is opened here
```

Nicodimus then reviewed and merged PR #5 on GitHub. PR #7 immediately showed **"This branch has
conflicts that must be resolved"**. He resolved it locally:

```bash
git switch main
git pull origin main                   # now contains step 5
git switch feature/07-appointment-service
git merge main                         # CONFLICT (content): Merge conflict in database/schema.py
# keep both blocks in database/schema.py (see 07_MERGE_CONFLICT_SCENARIO.md)
git add database/schema.py
git commit -m "Merge main into feature/07-appointment-service and resolve schema.py conflict"
git push
```

After the push the notice changed to **"No conflicts with base branch"**.

**Merge:** Yeukai reviews the resolved file, approves and merges with *Create a merge commit* (`Merge pull request #7 ...`). Full details: `docs/07_MERGE_CONFLICT_SCENARIO.md`.

---

## Step 8 - Medical record and Dashboard services (Nicodimus)

| Item | Detail |
| --- | --- |
| **Goal** | Implement `MedicalRecordService` (history, appointment linking) and `DashboardService`; add the `medical_records` table. |
| **Branch** | `feature/08-record-and-dashboard-services` |
| **Files** | `services/medical_record_service.py`, `services/dashboard_service.py`, `database/schema.py` (final version), `tests/test_medical_record_service.py`, `tests/test_dashboard_service.py`, `tests/test_schema_relationships.py` |
| **Reviewer** | Yeukai |
| **PR** | #8 `Step 8: MedicalRecordService, DashboardService and medical_records table` |

This branch is built on top of step 7 so that the two schema changes fit together without a second conflict. PR #8 is therefore merged after PR #7.

```bash
git switch -c feature/08-record-and-dashboard-services
git add services/medical_record_service.py
git commit -m "Add MedicalRecordService with history and appointment linking"
git add services/dashboard_service.py
git commit -m "Add DashboardService"
git add tests/
git commit -m "Add record, dashboard and schema relationship tests"
git push -u origin feature/08-record-and-dashboard-services
# later:
git merge feature/07-appointment-service -m "Merge feature/07-appointment-service into feature/08-record-and-dashboard-services"
git add database/schema.py              # final schema: adds the medical_records table
git commit -m "Add medical_records table to the schema"
git push
```

**Merge:** Yeukai approves and merges with *Create a merge commit* (`Merge pull request #8 ...`).

---

## Step 9 - Console menus and entry point (Nicodimus)

| Item | Detail |
| --- | --- |
| **Goal** | Build the menu-driven interface and `main.py`, and test the whole program with scripted input and a persistence test. |
| **Branch** | `feature/09-console-menus` |
| **Files** | `ui/__init__.py`, `ui/console.py`, `ui/menus.py`, `main.py`, `tests/test_menus.py`, `tests/test_persistence.py` |
| **Reviewer** | Yeukai |
| **PR** | #9 `Step 9: Console menus and main entry point` |

```bash
git switch -c feature/09-console-menus
git add ui/__init__.py ui/console.py
git commit -m "Add Console input/output helper"
git add ui/menus.py
git commit -m "Add abstract Menu and the five menu classes"
git add main.py
git commit -m "Add main.py entry point"
git add tests/
git commit -m "Add menu and persistence tests"
git push -u origin feature/09-console-menus
```

**Merge:** Yeukai approves and merges with *Create a merge commit* (`Merge pull request #9 ...`).

---

## Step 10 - Documentation, final testing and release (Yeukai)

| Item | Detail |
| --- | --- |
| **Goal** | Add the OOP mapping, collaboration evidence documents, testing document, compliance check and project report; update the README; run the full test suite; tag the release. |
| **Branch** | `feature/10-final-docs-and-release` |
| **Files** | `docs/03_OOP_MAPPING.md`, `docs/05_GITHUB_COLLABORATION_PLAN.md`, `docs/06_PULL_REQUEST_STRATEGY.md`, `docs/07_MERGE_CONFLICT_SCENARIO.md`, `docs/08_EVIDENCE_OF_COLLABORATION.md`, `docs/09_PROJECT_REPORT.md`, `docs/10_TESTING.md`, `docs/12_COMPLIANCE_CHECK.md`, `README.md` |
| **Reviewer** | Nicodimus |
| **PR** | #10 `Step 10: Final documentation, report and release v1.0.0` |

```bash
git switch main && git pull origin main
python -m unittest discover -s tests -t . -v      # must report: Ran 119 tests ... OK
git switch -c feature/10-final-docs-and-release
git add docs/05_GITHUB_COLLABORATION_PLAN.md docs/06_PULL_REQUEST_STRATEGY.md docs/07_MERGE_CONFLICT_SCENARIO.md docs/08_EVIDENCE_OF_COLLABORATION.md
git commit -m "Add GitHub collaboration documents"
git add docs/03_OOP_MAPPING.md docs/10_TESTING.md docs/12_COMPLIANCE_CHECK.md
git commit -m "Add OOP mapping, testing and compliance documents"
git add docs/09_PROJECT_REPORT.md
git commit -m "Add project report"
git add README.md
git commit -m "Update README contributors"
git push -u origin feature/10-final-docs-and-release
```

**Merge process:** Nicodimus approves; Yeukai merges with *Create a merge commit* (`Merge pull request #10 ...`), then tags the release:

```bash
git switch main && git pull origin main
git tag -a v1.0.0 -m "EHR Management System 1.0.0 - final submission"
git push origin v1.0.0
```

Before submitting, a fresh clone proves the program works from scratch:

```bash
git clone https://github.com/yeumawuka-stack/OOP_Mini_Project.git EHR-check
cd EHR-check
python -m unittest discover -s tests -t .
python main.py
```

Submit the repository link and the project report (`docs/09_PROJECT_REPORT.md`, exported to Word).
