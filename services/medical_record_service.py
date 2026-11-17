"""Medical record service: clinical notes, patient history and SQLite access."""

from models.appointment import Appointment
from models.medical_record import MedicalRecord
from services.base_service import BaseService
from utils.exceptions import BusinessRuleError, NotFoundError


class MedicalRecordService(BaseService):
    """INHERITANCE: extends BaseService.

    POLYMORPHISM: create(), update() and search() are overridden. A record may be
    linked to an appointment; linking completes that appointment automatically.
    """

    @property
    def table_name(self):
        return "medical_records"

    @property
    def entity_label(self):
        return "medical record"

    @property
    def columns(self):
        return (
            "patient_id", "doctor_id", "appointment_id", "visit_date",
            "diagnosis", "treatment", "prescription", "notes",
        )

    def _from_row(self, row):
        return MedicalRecord.from_row(row)

    def _check_links(self, record):
        """Validate patient, doctor and appointment; return the appointment status."""
        self._require_exists("patients", record.patient_id, "patient")
        self._require_exists("doctors", record.doctor_id, "doctor")
        if record.appointment_id is None:
            return None
        row = self._db.fetch_one(
            "SELECT patient_id, status FROM appointments WHERE id = ?",
            (record.appointment_id,),
        )
        if row is None:
            raise NotFoundError(f"No appointment found with ID {record.appointment_id}.")
        if row["patient_id"] != record.patient_id:
            raise BusinessRuleError("That appointment belongs to a different patient.")
        if row["status"] == Appointment.CANCELLED:
            raise BusinessRuleError("A medical record cannot be linked to a cancelled appointment.")
        return row["status"]

    def _complete_appointment(self, appointment_id):
        self._db.execute(
            "UPDATE appointments SET status = 'Completed' WHERE id = ?", (appointment_id,)
        )

    def create(self, record):
        status = self._check_links(record)
        self._insert(record)
        if status == Appointment.SCHEDULED:
            self._complete_appointment(record.appointment_id)
        return record

    def update(self, record):
        self.get_by_id(record.id)
        status = self._check_links(record)
        self._update_row(record)
        if status == Appointment.SCHEDULED:
            self._complete_appointment(record.appointment_id)
        return record

    def search(self, keyword):
        pattern = self._pattern(keyword)
        rows = self._db.fetch_all(
            "SELECT * FROM medical_records WHERE diagnosis LIKE ? OR treatment LIKE ? "
            "OR prescription LIKE ? ORDER BY visit_date DESC, id DESC",
            (pattern, pattern, pattern),
        )
        return [self._from_row(row) for row in rows]

    def get_history(self, patient_id):
        """Return all records of one patient, newest visit first."""
        self._require_exists("patients", patient_id, "patient")
        rows = self._db.fetch_all(
            "SELECT * FROM medical_records WHERE patient_id = ? "
            "ORDER BY visit_date DESC, id DESC",
            (patient_id,),
        )
        return [self._from_row(row) for row in rows]

    def get_history_details(self, patient_id):
        """Return a patient's history joined with doctor names (list of dicts)."""
        self._require_exists("patients", patient_id, "patient")
        rows = self._db.fetch_all(
            "SELECT m.id, m.visit_date, m.diagnosis, m.treatment, m.prescription, "
            "m.notes, m.appointment_id, m.doctor_id, "
            "d.first_name || ' ' || d.last_name AS doctor_name "
            "FROM medical_records m JOIN doctors d ON d.id = m.doctor_id "
            "WHERE m.patient_id = ? ORDER BY m.visit_date DESC, m.id DESC",
            (patient_id,),
        )
        return [dict(row) for row in rows]
