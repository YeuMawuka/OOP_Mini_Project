# Part 6 - Pull Request Strategy

Rules for every pull request:

- One PR per step, created from a `feature/NN-...` branch into `main`. Nobody commits directly to `main` (agreed team rule; GitHub branch protection is not available for private repositories on a free plan).
- The author and the reviewer are always different people: **Yeukai reviews Nicodimus's PRs (#1-#3 and #6-#9); Nicodimus reviews Yeukai's PRs (#4, #5 and #10).**
- The PR description lists *What this adds*, the files touched and any review notes.
- The reviewer reads **Files changed**, leaves line comments where needed, then chooses Approve or Request changes.
- A PR is merged only after the other student has reviewed it, with **Create a merge commit**. The remote branch is **kept** (do not click "Delete branch") so the lecturer can see it on the Branches page.
- Tests (`python -m unittest discover -s tests -t .`) must pass before the PR is opened.
- PRs were opened in numerical order (#1 first, #10 last) so the numbers on GitHub match the step numbers.

Suggested PR description template:

```markdown
## What this adds
<bullet list of the classes, tables and files>

## Review notes
<anything the reviewer should check or any ordering requirement>
```

## Summary

| PR | Title | Author | Reviewer | Merged by | Branch |
| --- | --- | --- | --- | --- | --- |
| #1 | Step 1: Project set-up, README and system design | Nicodimus | Yeukai | Nicodimus | `feature/01-project-setup` |
| #2 | Step 2: Utility classes (exceptions, validators, formatter) | Nicodimus | Yeukai | Nicodimus | `feature/02-utilities` |
| #3 | Step 3: Base Entity, Person, Patient and Doctor classes | Nicodimus | Yeukai | Nicodimus | `feature/03-person-models` |
| #4 | Step 4: Database connection, schema and BaseService | Yeukai | Nicodimus | Yeukai | `feature/04-database-layer` |
| #5 | Step 5: PatientService and DoctorService | Yeukai | Nicodimus | Nicodimus (after review, once PR #7 was open) | `feature/05-patient-doctor-services` |
| #6 | Step 6: Appointment and MedicalRecord classes | Nicodimus | Yeukai | Yeukai | `feature/06-appointment-record-models` |
| #7 | Step 7: AppointmentService and appointments table | Nicodimus | Yeukai | Yeukai (after the `schema.py` conflict was resolved) | `feature/07-appointment-service` |
| #8 | Step 8: MedicalRecordService, DashboardService and medical_records table | Nicodimus | Yeukai | Yeukai (after #7) | `feature/08-record-and-dashboard-services` |
| #9 | Step 9: Console menus and main entry point | Nicodimus | Yeukai | Yeukai | `feature/09-console-menus` |
| #10 | Step 10: Final documentation, report and release v1.0.0 | Yeukai | Nicodimus | Yeukai, then tag `v1.0.0` | `feature/10-final-docs-and-release` |

Every PR was merged with a merge commit, so each has a commit named `Merge pull request #N from ...` on `main`. The review events of each PR (comments and approvals) are shown on its **Conversation** tab.

Tests passing on `main` after each merge: #2: 22, #3: 34, #4: 40, #5: 57, #6: 69, #7: 85, #8: 108, #9: 119.

---

## PR #1 - Step 1: Project set-up, README and system design

- **Author:** Nicodimus **Reviewer:** Yeukai
- **Files changed:** `.gitignore`, `requirements.txt`, `README.md`, `docs/01_SYSTEM_DESIGN.md`, `docs/02_REPOSITORY_STRUCTURE.md`, and the removal of the misnamed `,gitignore`
- **What the reviewer checks:** `.gitignore` excludes `*.db` and `data/` so patient data is never published; the README run instructions are clear.

## PR #2 - Step 2: Utility classes (exceptions, validators, formatter)

- **Author:** Nicodimus **Reviewer:** Yeukai
- **Files changed (7):** `utils/__init__.py`, `utils/exceptions.py`, `utils/validators.py`, `utils/formatters.py`, `tests/__init__.py`, `tests/test_validators.py`, `tests/test_formatters.py`
- **What the reviewer checks:** the exception hierarchy, that every validator raises a clear error, and that the validators have unit tests for both valid and invalid input.

## PR #3 - Step 3: Base Entity, Person, Patient and Doctor classes

- **Author:** Nicodimus **Reviewer:** Yeukai
- **Files changed (7):** `models/__init__.py`, `models/base_entity.py`, `models/person.py`, `models/patient.py`, `models/doctor.py`, `tests/helpers.py`, `tests/test_person_models.py`
- **What the reviewer checks:** `BaseEntity` and `Person` cannot be instantiated, setters validate, and `Patient.describe()` and `Doctor.describe()` override the parent contract.

## PR #4 - Step 4: Database connection, schema and BaseService

- **Author:** Yeukai **Reviewer:** Nicodimus
- **Files changed (7):** `database/__init__.py`, `database/connection.py`, `database/schema.py`, `services/__init__.py`, `services/base_service.py`, `docs/04_DATABASE_DESIGN.md`, `tests/test_database.py`
- **What the reviewer checks:** SQL uses `?` placeholders (no string-built values), `PRAGMA foreign_keys = ON` is set, and `BaseService` is abstract. 40 tests pass on `main` afterwards.

## PR #5 - Step 5: PatientService and DoctorService

- **Author:** Yeukai **Reviewer:** Nicodimus
- **Files changed (5):** `services/patient_service.py`, `services/doctor_service.py`, `database/schema.py`, `tests/test_patient_service.py`, `tests/test_doctor_service.py`
- **What the reviewer checks:** each service overrides `create`, `update` and `search`, and duplicates raise `DuplicateError`.
- **Merge note:** merged after Nicodimus opened PR #7. This merge is what makes PR #7 conflict in `database/schema.py`.

## PR #6 - Step 6: Appointment and MedicalRecord classes

- **Author:** Nicodimus **Reviewer:** Yeukai
- **Files changed (3):** `models/appointment.py`, `models/medical_record.py`, `tests/test_clinical_models.py`
- **What the reviewer checks:** both classes inherit `BaseEntity`, validate in setters, and `Appointment.cancel()` refuses to cancel a completed appointment.

## PR #7 - Step 7: AppointmentService and appointments table

- **Author:** Nicodimus **Reviewer:** Yeukai
- **Commits (5):** Add AppointmentService with double-booking rule; Add appointment service tests; Merge main into feature/07-appointment-service; Add appointments table to the schema; Merge main into feature/07-appointment-service and resolve schema.py conflict
- **Files changed (3):** `database/schema.py`, `services/appointment_service.py`, `tests/test_appointment_service.py`
- **What the reviewer checks:** the double-booking rule, that cancelling keeps the row, and that the resolved `database/schema.py` contains **both** the search indexes from PR #5 and the `appointments` table with no conflict markers left. The conflict is described in `07_MERGE_CONFLICT_SCENARIO.md`.

## PR #8 - Step 8: MedicalRecordService, DashboardService and medical_records table

- **Author:** Nicodimus **Reviewer:** Yeukai
- **Files changed (6):** `database/schema.py`, `services/medical_record_service.py`, `services/dashboard_service.py`, `tests/test_medical_record_service.py`, `tests/test_dashboard_service.py`, `tests/test_schema_relationships.py`
- **What the reviewer checks:** a record cannot be linked to a cancelled appointment or another patient's appointment, and `ON DELETE SET NULL` protects clinical notes.
- **Order note:** the branch is built on top of PR #7, so #7 is merged first.

## PR #9 - Step 9: Console menus and main entry point

- **Author:** Nicodimus **Reviewer:** Yeukai
- **Files changed (6):** `ui/__init__.py`, `ui/console.py`, `ui/menus.py`, `main.py`, `tests/test_menus.py`, `tests/test_persistence.py`
- **What the reviewer checks:** an abstract `Menu` with five menu classes, `main.py` starts the main menu, and the persistence test proves records survive closing and reopening. 119 tests pass on `main` afterwards.

## PR #10 - Step 10: Final documentation, report and release v1.0.0

- **Author:** Yeukai **Reviewer:** Nicodimus
- **Files changed (9):** `docs/03_OOP_MAPPING.md`, `docs/05_GITHUB_COLLABORATION_PLAN.md`, `docs/06_PULL_REQUEST_STRATEGY.md`, `docs/07_MERGE_CONFLICT_SCENARIO.md`, `docs/08_EVIDENCE_OF_COLLABORATION.md`, `docs/09_PROJECT_REPORT.md`, `docs/10_TESTING.md`, `docs/12_COMPLIANCE_CHECK.md`, `README.md`
- **What the reviewer checks:** the report matches the code and the real history, and 119 tests pass from a fresh clone. After the merge the release tag `v1.0.0` is created on `main`.

## Review Checklist Used by Both Reviewers

1. Does every class have a docstring and a single clear job?
2. Are attributes private where the design says so, with validating setters?
3. Are abstract methods declared with `@abstractmethod` and overridden by the children?
4. Is every SQL statement parameterised with `?`?
5. Do the tests cover success, failure and edge cases, and do they all pass?
6. Is the commit history clear: small commits with meaningful messages?
