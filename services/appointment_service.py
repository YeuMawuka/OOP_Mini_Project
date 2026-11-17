"""Appointment service: scheduling rules and SQLite access."""

from models.appointment import Appointment
from services.base_service import BaseService
from utils.exceptions import BusinessRuleError
from utils.validators import Validators


class AppointmentService(BaseService):
    """INHERITANCE: extends BaseService.

    POLYMORPHISM: create(), update() and search() are overridden with scheduling
    rules: the patient and doctor must exist and a doctor cannot be booked twice
    for the same date and time.
    """

    @property
    def table_name(self):
        return "appointments"

    @property
    def entity_label(self):
        return "appointment"

    @property
    def columns(self):
        return (
            "patient_id", "doctor_id", "appointment_date", "appointment_time",
            "reason", "status",
        )

    def _from_row(self, row):
        return Appointment.from_row(row)

    def _ensure_doctor_free(self, appointment):
        row = self._db.fetch_one(
            "SELECT id FROM appointments WHERE doctor_id = ? AND appointment_date = ? "
            "AND appointment_time = ? AND status = 'Scheduled' AND id != ?",
            (appointment.doctor_id, appointment.appointment_date,
             appointment.appointment_time, appointment.id or 0),
        )
        if row is not None:
            raise BusinessRuleError(
                f"Doctor {appointment.doctor_id} already has appointment #{row['id']} "
                f"on {appointment.appointment_date} at {appointment.appointment_time}."
            )

    def _check_rules(self, appointment):
        self._require_exists("patients", appointment.patient_id, "patient")
        self._require_exists("doctors", appointment.doctor_id, "doctor")
        if appointment.status == Appointment.SCHEDULED:
            self._ensure_doctor_free(appointment)

    def create(self, appointment):
        self._check_rules(appointment)
        self._insert(appointment)
        return appointment

    def update(self, appointment):
        self.get_by_id(appointment.id)
        self._check_rules(appointment)
        self._update_row(appointment)
        return appointment

    def cancel(self, appointment_id):
        """Cancel an appointment; the row is kept so the history is preserved."""
        appointment = self.get_by_id(appointment_id)
        appointment.cancel()
        self._update_row(appointment)
        return appointment

    def search(self, keyword):
        pattern = self._pattern(keyword)
        rows = self._db.fetch_all(
            "SELECT * FROM appointments WHERE reason LIKE ? OR appointment_date LIKE ? "
            "OR status LIKE ? ORDER BY appointment_date, appointment_time",
            (pattern, pattern, pattern),
        )
        return [self._from_row(row) for row in rows]

    def list_details(self, patient_id=None, doctor_id=None, status=None):
        """Return appointments joined with patient and doctor names (list of dicts)."""
        conditions = []
        params = []
        if patient_id is not None:
            conditions.append("a.patient_id = ?")
            params.append(patient_id)
        if doctor_id is not None:
            conditions.append("a.doctor_id = ?")
            params.append(doctor_id)
        if status is not None:
            conditions.append("a.status = ?")
            params.append(Validators.choice(status, Validators.APPOINTMENT_STATUSES, "Status"))
        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        rows = self._db.fetch_all(
            "SELECT a.id, a.appointment_date, a.appointment_time, a.status, a.reason, "
            "a.patient_id, p.first_name || ' ' || p.last_name AS patient_name, "
            "a.doctor_id, d.first_name || ' ' || d.last_name AS doctor_name "
            "FROM appointments a "
            "JOIN patients p ON p.id = a.patient_id "
            "JOIN doctors d ON d.id = a.doctor_id "
            f"{where} ORDER BY a.appointment_date, a.appointment_time, a.id",
            tuple(params),
        )
        return [dict(row) for row in rows]

    def count_by_status(self):
        """Return a dictionary such as {'Scheduled': 2, 'Completed': 1, 'Cancelled': 0}."""
        totals = {status: 0 for status in Validators.APPOINTMENT_STATUSES}
        rows = self._db.fetch_all(
            "SELECT status, COUNT(*) AS total FROM appointments GROUP BY status"
        )
        for row in rows:
            totals[row["status"]] = row["total"]
        return totals
