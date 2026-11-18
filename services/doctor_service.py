"""Doctor service: doctor management and SQLite access."""

from models.doctor import Doctor
from services.base_service import BaseService
from utils.exceptions import DuplicateError


class DoctorService(BaseService):
    """INHERITANCE: extends BaseService.

    POLYMORPHISM: create(), update() and search() override the abstract methods
    with doctor-specific behaviour (National ID and license uniqueness).
    """

    @property
    def table_name(self):
        return "doctors"

    @property
    def entity_label(self):
        return "doctor"

    @property
    def columns(self):
        return (
            "first_name", "last_name", "national_id", "date_of_birth", "gender",
            "phone", "email", "specialization", "license_number", "department",
        )

    def _from_row(self, row):
        return Doctor.from_row(row)

    def _check_unique(self, doctor, ignore_id=None):
        ignore = ignore_id or 0
        if self._db.fetch_one(
            "SELECT id FROM doctors WHERE national_id = ? AND id != ?",
            (doctor.national_id, ignore),
        ):
            raise DuplicateError(
                f"A doctor with National ID {doctor.national_id} is already registered."
            )
        if self._db.fetch_one(
            "SELECT id FROM doctors WHERE license_number = ? AND id != ?",
            (doctor.license_number, ignore),
        ):
            raise DuplicateError(
                f"A doctor with license number {doctor.license_number} is already registered."
            )

    def create(self, doctor):
        self._check_unique(doctor)
        self._insert(doctor)
        return doctor

    def update(self, doctor):
        self._check_unique(doctor, doctor.id)
        self._update_row(doctor)
        return doctor

    def search(self, keyword):
        pattern = self._pattern(keyword)
        rows = self._db.fetch_all(
            "SELECT * FROM doctors WHERE first_name LIKE ? OR last_name LIKE ? "
            "OR (first_name || ' ' || last_name) LIKE ? OR specialization LIKE ? "
            "OR license_number LIKE ? OR department LIKE ? ORDER BY last_name, first_name",
            (pattern, pattern, pattern, pattern, pattern, pattern),
        )
        return [self._from_row(row) for row in rows]
