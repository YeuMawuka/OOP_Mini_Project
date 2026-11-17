# EHR-System: Electronic Health Record Management System

A menu-driven Electronic Health Record (EHR) system written in pure Python 3 with SQLite storage.
It was built as the Object-Oriented Programming mini project for the MSc Medical Analytics and
Informatics programme (University of Zimbabwe), and is designed around a Zimbabwean clinic:
National ID format `63-123456-A-42`, `+263` / `07x` phone numbers, the ten provinces of Zimbabwe
and MDPCZ-style practitioner licence numbers.

## Project Overview

The system lets clinic staff register patients and doctors, book appointments, write medical
records and read a patient's history. Everything is saved in a SQLite file, so data is still there
after the program is closed and reopened. The code demonstrates the four OOP pillars
(encapsulation, inheritance, polymorphism and abstraction) and was developed by two students
using Git branches, pull requests, code reviews and merge-conflict resolution on GitHub.

## Features

- **Patient management:** register, search, update, delete, view one patient, view all patients.
- **Doctor management:** register, search, update, delete, view one doctor, view all doctors.
- **Appointment management:** create, update, cancel (history is kept), view with filters
  (all / by patient / by doctor / by status). A doctor cannot be booked twice for the same slot.
- **Medical records:** create, update, view a patient's full medical history (newest first), view
  one record. Linking a record to a scheduled appointment marks that appointment as Completed.
- **Dashboard:** total patients, doctors, appointments and medical records, plus appointments by status.
- **Validation:** National ID, phone, email, dates, times, blood group, province and licence number.
- **Safe errors:** mistakes show a friendly message instead of a crash.
- **119 automated unit tests** covering models, validators, services, persistence and the menus.

## Technologies

- Python 3.9 or newer (tested on 3.13)
- Python standard library only: `sqlite3`, `abc`, `unittest`, `re`, `datetime`, `os`, `tempfile`
- Git and GitHub for version control and collaboration

## Installation

1. Install Python 3 from https://www.python.org/downloads/ (tick "Add Python to PATH" on Windows).
2. Install Git from https://git-scm.com/downloads.
3. Clone the repository (replace the address with your own repository link):

   ```bash
   git clone https://github.com/<your-username>/EHR-System.git
   cd EHR-System
   ```

No `pip install` is needed because there are no third-party packages (see `requirements.txt`).

## Usage

Menus are navigated by typing the number of an option and pressing Enter. Type `0` to go back or exit.
When updating a record, press Enter on any question to keep the value shown in square brackets.

Typical first session:

1. `2` Doctor management, then `1` Register doctor.
2. `1` Patient management, then `1` Register patient.
3. `3` Appointment management, then `1` Create appointment (use the IDs you were given).
4. `4` Medical records, then `1` Create medical record, then `2` to view the history.
5. `5` Dashboard to see the totals.

## Running the System

```bash
python main.py
```

On some systems the command is `python3 main.py` or `py main.py`.

Run the automated tests:

```bash
python -m unittest discover -s tests -t . -v
```

## Database Setup

No manual setup is required. On first start the program creates `data/ehr.db` and all tables
(`patients`, `doctors`, `appointments`, `medical_records`) automatically. The `data/` folder is
listed in `.gitignore` so real patient data is never uploaded to GitHub. To start with an empty
system, close the program and delete the `data/` folder. The full schema is in
`database/schema.py` and explained in `docs/04_DATABASE_DESIGN.md`.

## Project Structure

```text
EHR-System/
├── main.py                 program entry point
├── models/                 entity classes (abstraction, inheritance, encapsulation)
├── services/               business rules and SQLite access
├── database/               connection wrapper and schema
├── ui/                     console helper and menus
├── utils/                  exceptions, validators, formatters
├── tests/                  unit tests
└── docs/                   design, Git plan, report and compliance documents
```

## Contributors

| Name | Role in the project |
| --- | --- |
| Yeukai | Project set-up, utilities, abstract base class, Person/Patient/Doctor classes, database layer, patient and doctor services (steps 1-5) |
| Nicodimus | Appointment and MedicalRecord classes, appointment/record/dashboard services, console menus, final tests, documentation and report (steps 6-10) |

Each contribution can be verified in the GitHub commit history, pull requests and contribution graph.
