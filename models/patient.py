"""Patient: a person who receives care."""

from models.person import Person
from utils.validators import Validators


class Patient(Person):
    """INHERITANCE: Patient is a Person with medical and contact details.

    POLYMORPHISM: get_role(), describe() and to_dict() override the versions
    declared in the parent classes.
    """

    def __init__(self, first_name, last_name, national_id, date_of_birth,
                 gender, phone, email="", address="", province="Harare",
                 blood_group="Unknown", allergies="", emergency_contact_name="",
                 emergency_contact_phone="", entity_id=None):
        super().__init__(first_name, last_name, national_id, date_of_birth,
                         gender, phone, email, entity_id)
        self.address = address
        self.province = province
        self.blood_group = blood_group
        self.allergies = allergies
        self.emergency_contact_name = emergency_contact_name
        self.emergency_contact_phone = emergency_contact_phone

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = Validators.text(value, "Address", 200, required=False)

    @property
    def province(self):
        return self.__province

    @province.setter
    def province(self, value):
        self.__province = Validators.choice(value, Validators.PROVINCES, "Province")

    @property
    def blood_group(self):
        return self.__blood_group

    @blood_group.setter
    def blood_group(self, value):
        self.__blood_group = Validators.choice(value, Validators.BLOOD_GROUPS, "Blood group")

    @property
    def allergies(self):
        return self.__allergies

    @allergies.setter
    def allergies(self, value):
        self.__allergies = Validators.text(value, "Allergies", 300, required=False)

    @property
    def emergency_contact_name(self):
        return self.__emergency_contact_name

    @emergency_contact_name.setter
    def emergency_contact_name(self, value):
        self.__emergency_contact_name = Validators.name(
            value, "Emergency contact name", required=False
        )

    @property
    def emergency_contact_phone(self):
        return self.__emergency_contact_phone

    @emergency_contact_phone.setter
    def emergency_contact_phone(self, value):
        self.__emergency_contact_phone = Validators.phone(
            value, "Emergency contact phone", required=False
        )

    def get_role(self):
        return "Patient"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "address": self.address,
            "province": self.province,
            "blood_group": self.blood_group,
            "allergies": self.allergies,
            "emergency_contact_name": self.emergency_contact_name,
            "emergency_contact_phone": self.emergency_contact_phone,
        })
        return data

    def describe(self):
        lines = [f"Patient #{self.id}: {self.full_name}"]
        lines.extend(self._identity_lines())
        lines.extend([
            f"  Address       : {self.address or 'not provided'}, {self.province}",
            f"  Blood group   : {self.blood_group}",
            f"  Allergies     : {self.allergies or 'none recorded'}",
            f"  Emergency     : {self.emergency_contact_name or 'not provided'}"
            f" ({self.emergency_contact_phone or 'no phone'})",
        ])
        return "\n".join(lines)

    @classmethod
    def from_row(cls, row):
        """Build a Patient from a database row."""
        return cls(
            first_name=row["first_name"],
            last_name=row["last_name"],
            national_id=row["national_id"],
            date_of_birth=row["date_of_birth"],
            gender=row["gender"],
            phone=row["phone"],
            email=row["email"],
            address=row["address"],
            province=row["province"],
            blood_group=row["blood_group"],
            allergies=row["allergies"],
            emergency_contact_name=row["emergency_contact_name"],
            emergency_contact_phone=row["emergency_contact_phone"],
            entity_id=row["id"],
        )
