"""Menu classes for the console interface."""

from abc import ABC, abstractmethod

from models.appointment import Appointment
from models.doctor import Doctor
from models.medical_record import MedicalRecord
from models.patient import Patient
from utils.exceptions import EHRError
from utils.formatters import TableFormatter
from utils.validators import Validators


class Menu(ABC):
    """ABSTRACTION: a menu has a title and options; run() drives the loop.

    POLYMORPHISM: every subclass supplies its own title and options, but all of
    them are started with the same run() call.
    """

    exit_label = "Back"

    def __init__(self, console):
        self._console = console

    @property
    @abstractmethod
    def title(self):
        """Heading shown above the options."""

    @abstractmethod
    def options(self):
        """Return a list of (label, handler) pairs."""

    def run(self):
        while True:
            choices = self.options()
            self._console.say("")
            self._console.say(TableFormatter.heading(self.title))
            for number, (label, _handler) in enumerate(choices, start=1):
                self._console.say(f"  {number}. {label}")
            self._console.say(f"  0. {self.exit_label}")
            answer = self._console.read("Choose an option: ").strip()
            if answer == "0":
                return
            if answer.isdigit() and 1 <= int(answer) <= len(choices):
                handler = choices[int(answer) - 1][1]
                try:
                    handler()
                except EHRError as error:
                    self._console.say(f"Error: {error}")
            else:
                self._console.say("Invalid option. Please type one of the numbers shown.")


class PatientMenu(Menu):
    """Register, search, update, delete and view patients."""

    def __init__(self, console, patient_service):
        super().__init__(console)
        self._service = patient_service

    @property
    def title(self):
        return "Patient Management"

    def options(self):
        return [
            ("Register patient", self.register),
            ("Search patient", self.search),
            ("Update patient", self.update),
            ("Delete patient", self.delete),
            ("View patient", self.view),
            ("View all patients", self.view_all),
        ]

    def _collect(self, current=None):
        ask = self._console.ask

        def value(name, default=None):
            return getattr(current, name) if current is not None else default

        return {
            "first_name": ask("First name", lambda v: Validators.name(v, "First name"),
                              value("first_name")),
            "last_name": ask("Last name", lambda v: Validators.name(v, "Last name"),
                             value("last_name")),
            "national_id": ask("National ID (e.g. 63-123456-A-42)", Validators.national_id,
                               value("national_id")),
            "date_of_birth": ask("Date of birth (YYYY-MM-DD)", Validators.date_of_birth,
                                 value("date_of_birth")),
            "gender": self._console.ask_choice("Gender", Validators.GENDERS, value("gender")),
            "phone": ask("Phone (e.g. 0771234567)", Validators.phone, value("phone")),
            "email": ask("Email (optional)", Validators.email, value("email"), required=False),
            "address": ask("Address (optional)", lambda v: Validators.text(v, "Address", 200),
                           value("address"), required=False),
            "province": self._console.ask_choice(
                "Province", Validators.PROVINCES, value("province", "Harare")),
            "blood_group": self._console.ask_choice(
                "Blood group", Validators.BLOOD_GROUPS, value("blood_group", "Unknown")),
            "allergies": ask("Allergies (optional)",
                             lambda v: Validators.text(v, "Allergies", 300),
                             value("allergies"), required=False),
            "emergency_contact_name": ask(
                "Emergency contact name (optional)",
                lambda v: Validators.name(v, "Emergency contact name"),
                value("emergency_contact_name"), required=False),
            "emergency_contact_phone": ask(
                "Emergency contact phone (optional)",
                lambda v: Validators.phone(v, "Emergency contact phone"),
                value("emergency_contact_phone"), required=False),
        }

    def register(self):
        patient = Patient(**self._collect())
        self._service.create(patient)
        self._console.say(f"Patient registered with ID {patient.id}.")

    def search(self):
        keyword = self._console.ask("Search by name, National ID or phone")
        self._show_table(self._service.search(keyword))

    def update(self):
        patient = self._service.get_by_id(self._console.ask_id("Patient ID to update"))
        self._console.say(patient.describe())
        self._console.say("Press Enter to keep the value shown in brackets.")
        for name, value in self._collect(patient).items():
            setattr(patient, name, value)
        self._service.update(patient)
        self._console.say("Patient updated.")

    def delete(self):
        patient = self._service.get_by_id(self._console.ask_id("Patient ID to delete"))
        self._console.say(patient.describe())
        if self._console.confirm(
            "Deleting this patient also deletes their appointments and medical records. Continue?"
        ):
            self._service.delete(patient.id)
            self._console.say("Patient deleted.")
        else:
            self._console.say("Deletion cancelled.")

    def view(self):
        patient = self._service.get_by_id(self._console.ask_id("Patient ID"))
        self._console.say(patient.describe())

    def view_all(self):
        self._show_table(self._service.list_all())

    def _show_table(self, patients):
        rows = [
            (p.id, p.full_name, p.national_id, p.age, p.gender, p.phone, p.province)
            for p in patients
        ]
        self._console.say(TableFormatter.render(
            ("ID", "Name", "National ID", "Age", "Gender", "Phone", "Province"), rows))


class DoctorMenu(Menu):
    """Register, search, update, delete and view doctors."""

    def __init__(self, console, doctor_service):
        super().__init__(console)
        self._service = doctor_service

    @property
    def title(self):
        return "Doctor Management"

    def options(self):
        return [
            ("Register doctor", self.register),
            ("Search doctor", self.search),
            ("Update doctor", self.update),
            ("Delete doctor", self.delete),
            ("View doctor", self.view),
            ("View all doctors", self.view_all),
        ]

    def _collect(self, current=None):
        ask = self._console.ask

        def value(name, default=None):
            return getattr(current, name) if current is not None else default

        return {
            "first_name": ask("First name", lambda v: Validators.name(v, "First name"),
                              value("first_name")),
            "last_name": ask("Last name", lambda v: Validators.name(v, "Last name"),
                             value("last_name")),
            "national_id": ask("National ID (e.g. 08-765432-B-12)", Validators.national_id,
                               value("national_id")),
            "date_of_birth": ask("Date of birth (YYYY-MM-DD)", Validators.date_of_birth,
                                 value("date_of_birth")),
            "gender": self._console.ask_choice("Gender", Validators.GENDERS, value("gender")),
            "phone": ask("Phone (e.g. +263772000111)", Validators.phone, value("phone")),
            "email": ask("Email (optional)", Validators.email, value("email"), required=False),
            "specialization": ask("Specialization",
                                  lambda v: Validators.text(v, "Specialization", 80),
                                  value("specialization")),
            "license_number": ask("License number (e.g. MDPCZ-10234)",
                                  Validators.license_number, value("license_number")),
            "department": ask("Department", lambda v: Validators.text(v, "Department", 80),
                              value("department", "Outpatient")),
        }

    def register(self):
        doctor = Doctor(**self._collect())
        self._service.create(doctor)
        self._console.say(f"Doctor registered with ID {doctor.id}.")

    def search(self):
        keyword = self._console.ask("Search by name, specialization, license or department")
        self._show_table(self._service.search(keyword))

    def update(self):
        doctor = self._service.get_by_id(self._console.ask_id("Doctor ID to update"))
        self._console.say(doctor.describe())
        self._console.say("Press Enter to keep the value shown in brackets.")
        for name, value in self._collect(doctor).items():
            setattr(doctor, name, value)
        self._service.update(doctor)
        self._console.say("Doctor updated.")

    def delete(self):
        doctor = self._service.get_by_id(self._console.ask_id("Doctor ID to delete"))
        self._console.say(doctor.describe())
        if self._console.confirm("Delete this doctor?"):
            self._service.delete(doctor.id)
            self._console.say("Doctor deleted.")
        else:
            self._console.say("Deletion cancelled.")

    def view(self):
        doctor = self._service.get_by_id(self._console.ask_id("Doctor ID"))
        self._console.say(doctor.describe())

    def view_all(self):
        self._show_table(self._service.list_all())

    def _show_table(self, doctors):
        rows = [
            (d.id, d.full_name, d.specialization, d.license_number, d.department, d.phone)
            for d in doctors
        ]
        self._console.say(TableFormatter.render(
            ("ID", "Name", "Specialization", "License", "Department", "Phone"), rows))


class AppointmentMenu(Menu):
    """Create, update, cancel and view appointments."""

    def __init__(self, console, appointment_service):
        super().__init__(console)
        self._service = appointment_service

    @property
    def title(self):
        return "Appointment Management"

    def options(self):
        return [
            ("Create appointment", self.create),
            ("Update appointment", self.update),
            ("Cancel appointment", self.cancel),
            ("View appointments", self.view),
        ]

    def create(self):
        ask = self._console.ask
        appointment = Appointment(
            patient_id=self._console.ask_id("Patient ID"),
            doctor_id=self._console.ask_id("Doctor ID"),
            appointment_date=ask("Appointment date (YYYY-MM-DD)", Validators.date_value),
            appointment_time=ask("Appointment time (HH:MM, 24-hour)", Validators.time_value),
            reason=ask("Reason for visit", lambda v: Validators.text(v, "Reason", 200)),
        )
        self._service.create(appointment)
        self._console.say(f"Appointment created with ID {appointment.id}.")

    def update(self):
        ask = self._console.ask
        appointment = self._service.get_by_id(self._console.ask_id("Appointment ID to update"))
        self._console.say(appointment.describe())
        self._console.say("Press Enter to keep the value shown in brackets.")
        appointment.doctor_id = ask(
            "Doctor ID", lambda v: Validators.positive_int(v, "Doctor ID"),
            appointment.doctor_id)
        appointment.appointment_date = ask(
            "Appointment date (YYYY-MM-DD)", Validators.date_value,
            appointment.appointment_date)
        appointment.appointment_time = ask(
            "Appointment time (HH:MM, 24-hour)", Validators.time_value,
            appointment.appointment_time)
        appointment.reason = ask(
            "Reason for visit", lambda v: Validators.text(v, "Reason", 200),
            appointment.reason)
        appointment.status = self._console.ask_choice(
            "Status", Validators.APPOINTMENT_STATUSES, appointment.status)
        self._service.update(appointment)
        self._console.say("Appointment updated.")

    def cancel(self):
        appointment = self._service.get_by_id(self._console.ask_id("Appointment ID to cancel"))
        self._console.say(appointment.describe())
        if self._console.confirm("Cancel this appointment?"):
            self._service.cancel(appointment.id)
            self._console.say("Appointment cancelled.")
        else:
            self._console.say("Cancellation aborted.")

    def view(self):
        self._console.say("  1. All appointments")
        self._console.say("  2. Appointments of one patient")
        self._console.say("  3. Appointments of one doctor")
        self._console.say("  4. Appointments with one status")
        answer = self._console.ask(
            "Filter", lambda v: Validators.choice(v, ("1", "2", "3", "4"), "Filter"))
        patient_id = doctor_id = status = None
        if answer == "2":
            patient_id = self._console.ask_id("Patient ID")
        elif answer == "3":
            doctor_id = self._console.ask_id("Doctor ID")
        elif answer == "4":
            status = self._console.ask_choice("Status", Validators.APPOINTMENT_STATUSES)
        details = self._service.list_details(patient_id, doctor_id, status)
        rows = [
            (a["id"], a["appointment_date"], a["appointment_time"], a["patient_name"],
             a["doctor_name"], a["status"], a["reason"])
            for a in details
        ]
        self._console.say(TableFormatter.render(
            ("ID", "Date", "Time", "Patient", "Doctor", "Status", "Reason"), rows))


class MedicalRecordMenu(Menu):
    """Create and update medical records and view patient history."""

    def __init__(self, console, record_service):
        super().__init__(console)
        self._service = record_service

    @property
    def title(self):
        return "Medical Records"

    def options(self):
        return [
            ("Create medical record", self.create),
            ("View patient medical history", self.history),
            ("Update medical record", self.update),
            ("View one medical record", self.view_one),
        ]

    def create(self):
        ask = self._console.ask
        patient_id = self._console.ask_id("Patient ID")
        doctor_id = self._console.ask_id("Doctor ID")
        appointment_id = ask(
            "Appointment ID (optional, press Enter to skip)",
            lambda v: Validators.positive_int(v, "Appointment ID"), required=False)
        record = MedicalRecord(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_id=appointment_id if appointment_id != "" else None,
            visit_date=ask("Visit date (YYYY-MM-DD)", Validators.date_value),
            diagnosis=ask("Diagnosis", lambda v: Validators.text(v, "Diagnosis", 200)),
            treatment=ask("Treatment", lambda v: Validators.text(v, "Treatment", 500)),
            prescription=ask("Prescription (optional)",
                             lambda v: Validators.text(v, "Prescription", 500),
                             required=False),
            notes=ask("Notes (optional)", lambda v: Validators.text(v, "Notes", 1000),
                      required=False),
        )
        self._service.create(record)
        self._console.say(f"Medical record created with ID {record.id}.")

    def history(self):
        patient_id = self._console.ask_id("Patient ID")
        details = self._service.get_history_details(patient_id)
        rows = [
            (r["id"], r["visit_date"], r["doctor_name"], r["diagnosis"], r["treatment"],
             r["prescription"])
            for r in details
        ]
        self._console.say(f"Medical history for patient {patient_id}: {len(rows)} record(s)")
        self._console.say(TableFormatter.render(
            ("ID", "Visit", "Doctor", "Diagnosis", "Treatment", "Prescription"), rows))

    def update(self):
        ask = self._console.ask
        record = self._service.get_by_id(self._console.ask_id("Medical record ID to update"))
        self._console.say(record.describe())
        self._console.say("Press Enter to keep the value shown in brackets.")
        record.visit_date = ask("Visit date (YYYY-MM-DD)", Validators.date_value,
                                record.visit_date)
        record.diagnosis = ask("Diagnosis", lambda v: Validators.text(v, "Diagnosis", 200),
                               record.diagnosis)
        record.treatment = ask("Treatment", lambda v: Validators.text(v, "Treatment", 500),
                               record.treatment)
        record.prescription = ask("Prescription",
                                  lambda v: Validators.text(v, "Prescription", 500),
                                  record.prescription, required=False)
        record.notes = ask("Notes", lambda v: Validators.text(v, "Notes", 1000),
                           record.notes, required=False)
        self._service.update(record)
        self._console.say("Medical record updated.")

    def view_one(self):
        record = self._service.get_by_id(self._console.ask_id("Medical record ID"))
        self._console.say(record.describe())


class MainMenu(Menu):
    """Top-level menu that opens every other menu."""

    exit_label = "Exit"

    def __init__(self, console, patient_menu, doctor_menu, appointment_menu,
                 record_menu, dashboard_service):
        super().__init__(console)
        self._patient_menu = patient_menu
        self._doctor_menu = doctor_menu
        self._appointment_menu = appointment_menu
        self._record_menu = record_menu
        self._dashboard = dashboard_service

    @property
    def title(self):
        return "Electronic Health Record (EHR) Management System"

    def options(self):
        return [
            ("Patient management", self._patient_menu.run),
            ("Doctor management", self._doctor_menu.run),
            ("Appointment management", self._appointment_menu.run),
            ("Medical records", self._record_menu.run),
            ("Dashboard", self.show_dashboard),
        ]

    def show_dashboard(self):
        self._console.say(self._dashboard.render())
