"""Doctor: a person who delivers care."""

from models.person import Person
from utils.validators import Validators


class Doctor(Person):
    """INHERITANCE: Doctor is a Person with professional details.

    POLYMORPHISM: get_role(), describe() and to_dict() override the parent
    versions, so a Doctor and a Patient answer the same calls differently.
    """

    def __init__(self, first_name, last_name, national_id, date_of_birth,
                 gender, phone, email="", specialization="General Practice",
                 license_number="MDPCZ-00000", department="Outpatient",
                 entity_id=None):
        super().__init__(first_name, last_name, national_id, date_of_birth,
                         gender, phone, email, entity_id)
        self.specialization = specialization
        self.license_number = license_number
        self.department = department

    @property
    def specialization(self):
        return self.__specialization

    @specialization.setter
    def specialization(self, value):
        self.__specialization = Validators.text(value, "Specialization", 80)

    @property
    def license_number(self):
        return self.__license_number

    @license_number.setter
    def license_number(self, value):
        self.__license_number = Validators.license_number(value)

    @property
    def department(self):
        return self.__department

    @department.setter
    def department(self, value):
        self.__department = Validators.text(value, "Department", 80)

    def get_role(self):
        return "Doctor"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "specialization": self.specialization,
            "license_number": self.license_number,
            "department": self.department,
        })
        return data

    def describe(self):
        lines = [f"Doctor #{self.id}: Dr. {self.full_name}"]
        lines.extend(self._identity_lines())
        lines.extend([
            f"  Specialization: {self.specialization}",
            f"  License number: {self.license_number}",
            f"  Department    : {self.department}",
        ])
        return "\n".join(lines)

    @classmethod
    def from_row(cls, row):
        """Build a Doctor from a database row."""
        return cls(
            first_name=row["first_name"],
            last_name=row["last_name"],
            national_id=row["national_id"],
            date_of_birth=row["date_of_birth"],
            gender=row["gender"],
            phone=row["phone"],
            email=row["email"],
            specialization=row["specialization"],
            license_number=row["license_number"],
            department=row["department"],
            entity_id=row["id"],
        )
