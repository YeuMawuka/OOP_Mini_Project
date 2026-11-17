"""Patient service: patient management and SQLite access."""

from models.patient import Patient
from services.base_service import BaseService
from utils.exceptions import DuplicateError


class PatientService(BaseService):
    """INHERITANCE: extends BaseService.

    POLYMORPHISM: create(), update() and search() override the abstract methods
    with patient-specific behaviour.
    """

    @property
    def table_name(self):
        return "patients"

    @property
    def entity_label(self):
        return "patient"

    @property
    def columns(self):
        return (
            "first_name", "last_name", "national_id", "date_of_birth", "gender",
            "phone", "email", "address", "province", "blood_group", "allergies",
            "emergency_contact_name", "emergency_contact_phone",
        )

    def _from_row(self, row):
        return Patient.from_row(row)

    def _national_id_in_use(self, national_id, ignore_id=None):
        row = self._db.fetch_one(
            "SELECT id FROM patients WHERE national_id = ? AND id != ?",
            (national_id, ignore_id or 0),
        )
        return row is not None

    def create(self, patient):
        if self._national_id_in_use(patient.national_id):
            raise DuplicateError(
                f"A patient with National ID {patient.national_id} is already registered."
            )
        self._insert(patient)
        return patient

    def update(self, patient):
        if self._national_id_in_use(patient.national_id, patient.id):
            raise DuplicateError(
                f"Another patient already uses National ID {patient.national_id}."
            )
        self._update_row(patient)
        return patient

    def search(self, keyword):
        pattern = self._pattern(keyword)
        rows = self._db.fetch_all(
            "SELECT * FROM patients WHERE first_name LIKE ? OR last_name LIKE ? "
            "OR (first_name || ' ' || last_name) LIKE ? OR national_id LIKE ? "
            "OR phone LIKE ? ORDER BY last_name, first_name",
            (pattern, pattern, pattern, pattern, pattern),
        )
        return [self._from_row(row) for row in rows]
