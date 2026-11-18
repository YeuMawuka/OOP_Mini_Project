"""Person: abstract parent class of Patient and Doctor."""

from abc import abstractmethod
from datetime import date

from models.base_entity import BaseEntity
from utils.validators import Validators


class Person(BaseEntity):
    """INHERITANCE: holds the data and behaviour that patients and doctors share.

    ENCAPSULATION: every field is a private attribute (double underscore) that is
    read through a property and written through a validating setter.
    ABSTRACTION: Person is abstract because get_role() and describe() have no
    implementation here; each child class must supply its own.
    """

    def __init__(self, first_name, last_name, national_id, date_of_birth,
                 gender, phone, email="", entity_id=None):
        super().__init__(entity_id)
        self.first_name = first_name
        self.last_name = last_name
        self.national_id = national_id
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone = phone
        self.email = email

    # ---- controlled access (getters and validating setters) -----------------
    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        self.__first_name = Validators.name(value, "First name")

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        self.__last_name = Validators.name(value, "Last name")

    @property
    def national_id(self):
        return self.__national_id

    @national_id.setter
    def national_id(self, value):
        self.__national_id = Validators.national_id(value)

    @property
    def date_of_birth(self):
        return self.__date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value):
        self.__date_of_birth = Validators.date_of_birth(value)

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, value):
        self.__gender = Validators.choice(value, Validators.GENDERS, "Gender")

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = Validators.phone(value)

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = Validators.email(value)

    # ---- behaviour shared by all people -------------------------------------
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        born = date.fromisoformat(self.date_of_birth)
        today = date.today()
        had_birthday = (today.month, today.day) >= (born.month, born.day)
        return today.year - born.year - (0 if had_birthday else 1)

    @abstractmethod
    def get_role(self):
        """Return the role of this person in the hospital (overridden)."""

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "national_id": self.national_id,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
        }

    def _identity_lines(self):
        """Lines of text common to every person, reused by child describe()."""
        return [
            f"  National ID   : {self.national_id}",
            f"  Date of birth : {self.date_of_birth} (age {self.age})",
            f"  Gender        : {self.gender}",
            f"  Phone         : {self.phone}",
            f"  Email         : {self.email or 'not provided'}",
        ]
