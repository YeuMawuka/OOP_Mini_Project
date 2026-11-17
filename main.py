"""Entry point of the EHR Management System.

Run it from the project folder with:  python main.py
"""

from database.connection import Database
from services.appointment_service import AppointmentService
from services.dashboard_service import DashboardService
from services.doctor_service import DoctorService
from services.medical_record_service import MedicalRecordService
from services.patient_service import PatientService
from ui.console import Console
from ui.menus import (
    AppointmentMenu,
    DoctorMenu,
    MainMenu,
    MedicalRecordMenu,
    PatientMenu,
)


def build_application(database, console):
    """Create the services and menus and return the main menu."""
    patients = PatientService(database)
    doctors = DoctorService(database)
    appointments = AppointmentService(database)
    records = MedicalRecordService(database)
    dashboard = DashboardService(patients, doctors, appointments, records)
    return MainMenu(
        console,
        PatientMenu(console, patients),
        DoctorMenu(console, doctors),
        AppointmentMenu(console, appointments),
        MedicalRecordMenu(console, records),
        dashboard,
    )


def main():
    console = Console()
    database = Database()
    console.say(f"Using database file: {database.path}")
    try:
        build_application(database, console).run()
        console.say("Goodbye.")
    except (EOFError, KeyboardInterrupt):
        console.say("\nSession ended.")
    finally:
        database.close()


if __name__ == "__main__":
    main()
