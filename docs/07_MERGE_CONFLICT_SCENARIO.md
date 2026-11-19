# Part 7 - Merge Conflict Scenario

This conflict is not invented: it was produced by running the plan in a practice repository, and
the text below is the real Git output.

## What Happens

Both students need to change `database/schema.py` at the same time:

- **Student A, Yeukai (step 5):** adds two search indexes for patients and doctors.
- **Student B, Nicodimus (step 7):** adds the `appointments` table and its two indexes.

Both start from the same `main` (which contains step 4) and both add text **in the same place**:
right after the `doctors` table, before the closing `"""` of `SCHEMA_SQL`. Yeukai's PR #5 is
merged first (Nicodimus, as the reviewer, merges it after approving it). When Nicodimus brings
`main` into his branch, Git cannot decide which new text comes first, so it stops and asks him.

## File Involved

`database/schema.py`

## Original Code (on `main` after step 4)

```python
    department TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""
```

## Student A (Yeukai) Changes - branch `feature/05-patient-doctor-services`

Commit "Add search indexes for patients and doctors":

```python
    department TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_patients_name ON patients (last_name, first_name);
CREATE INDEX IF NOT EXISTS idx_doctors_specialization ON doctors (specialization);
"""
```

## Student B (Nicodimus) Changes - branch `feature/07-appointment-service`

Commit "Add appointments table to the schema":

```python
    department TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

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
"""
```

## How the Conflict Appears

PR #5 is merged first. On GitHub, PR #7 now says **"This branch has conflicts that must be resolved"** for `database/schema.py`. Nicodimus runs:

```bash
git switch main
git pull origin main
git switch feature/07-appointment-service
git merge main
```

Git prints (this is the real output from the repository):

```text
Auto-merging database/schema.py
CONFLICT (content): Merge conflict in database/schema.py
Automatic merge failed; fix conflicts and then commit the result.
```

`git status --short` shows the file as `UU` (unmerged by both sides):

```text
UU database/schema.py
A  services/doctor_service.py
A  services/patient_service.py
A  tests/test_doctor_service.py
A  tests/test_patient_service.py
```

## Conflict Markers

Open `database/schema.py`. Near the end of the file it now contains:

```text
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

<<<<<<< HEAD
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
=======
CREATE INDEX IF NOT EXISTS idx_patients_name ON patients (last_name, first_name);
CREATE INDEX IF NOT EXISTS idx_doctors_specialization ON doctors (specialization);
>>>>>>> main
"""
```

How to read the markers:

| Marker | Meaning |
| --- | --- |
| `<<<<<<< HEAD` | Start of **your** version (Nicodimus's branch: the appointments table) |
| `=======` | Divider between the two versions |
| `>>>>>>> main` | End of the **incoming** version (from `main`: Yeukai's indexes) |

## Resolution Process

1. **Understand both changes.** They do not contradict each other: one adds indexes for patients and doctors, the other adds a new table. The correct result keeps **both**.
2. **Choose an order.** Yeukai's index lines are already on `main` and belong with the `patients` and `doctors` tables, so they go first; Nicodimus's appointments block goes after them.
3. **Edit the file:** remove the three marker lines (`<<<<<<< HEAD`, `=======`, `>>>>>>> main`) and arrange the text as shown below. Make sure no marker is left: `grep -c "<<<<<<<" database/schema.py` must print `0`. On the real repository the markers were on lines 41, 59 and 62 (`grep -n "<<<<<<<\|=======\|>>>>>>>" database/schema.py`), and the resolved file has 7 `CREATE` statements: three tables and four indexes at that point.
4. **Check the result:** `grep -n "CREATE" database/schema.py` lists the `patients`, `doctors` and `appointments` tables and their four indexes. The full test run (`Ran 119 tests ... OK`) is done after all pull requests are merged.
5. **Mark as resolved and complete the merge:** `git add database/schema.py` then `git commit -m "Merge main into feature/07-appointment-service and resolve schema.py conflict"`.
6. **Push:** `git push`. GitHub removes the conflict warning from PR #7.
7. **Ask Yeukai to re-check.** On GitHub PR #7 changes from "This branch has conflicts that must be resolved" to "No conflicts with base branch". The merged file is read by the other student before the PR is merged.

## Final Resolved Code

```python
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
"""
```

(Step 8 later appends the `medical_records` table after this block with no conflict, giving the final `database/schema.py` in the repository.)

## Git Commands Used (complete list)

```bash
# Yeukai (step 5) - pushed earlier
git push -u origin feature/05-patient-doctor-services
#   ... Nicodimus reviews PR #5 and merges it on GitHub (after PR #7 is open) ...

# Nicodimus (step 7) - was working in parallel
git switch main
git pull origin main                       # downloads Yeukai's merged step 5
git switch feature/07-appointment-service
git merge main                             # CONFLICT in database/schema.py
git status                                 # shows: both modified: database/schema.py
# ... edit database/schema.py, remove markers, keep both blocks ...
grep -c "<<<<<<<" database/schema.py        # 0 = no markers left
git add database/schema.py
git commit -m "Merge main into feature/07-appointment-service and resolve schema.py conflict"
git push
git log --oneline --graph --all            # shows the merge commit joining the two lines of work
```

If you get lost during a conflict, `git merge --abort` returns the branch to the state before
`git merge main` so you can start again.

## What the Lecturer Sees on GitHub

- PR #7 **Conversation** tab: the "This branch has conflicts" notice appeared, then disappeared after the push.
- PR #7 **Commits** tab: Nicodimus's commits, the clean merge commit "Merge main into feature/07-appointment-service", and the conflict-resolving merge commit "Merge main into feature/07-appointment-service and resolve schema.py conflict".
- **Insights > Network** graph: the two branches diverging and rejoining.
- `database/schema.py` on `main` contains no conflict markers.
