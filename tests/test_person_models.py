import unittest

from models.base_entity import BaseEntity
from models.doctor import Doctor
from models.patient import Patient
from models.person import Person
from tests.helpers import make_doctor, make_patient
from utils.exceptions import ValidationError


class AbstractionTests(unittest.TestCase):
    def test_base_entity_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            BaseEntity()

    def test_person_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Person("A", "B", "63-123456-A-42", "1990-01-01", "Male", "0771234567")


class InheritanceTests(unittest.TestCase):
    def test_patient_and_doctor_are_people_and_entities(self):
        self.assertTrue(issubclass(Patient, Person))
        self.assertTrue(issubclass(Doctor, Person))
        self.assertTrue(issubclass(Person, BaseEntity))

    def test_children_reuse_parent_behaviour(self):
        self.assertEqual(make_patient().full_name, "Tendai Moyo")
        self.assertEqual(make_doctor().full_name, "Farai Chikwanha")


class PolymorphismTests(unittest.TestCase):
    def test_same_call_different_result(self):
        people = [make_patient(), make_doctor()]
        self.assertEqual([p.get_role() for p in people], ["Patient", "Doctor"])
        self.assertIn("Patient #", people[0].describe())
        self.assertIn("Doctor #", people[1].describe())

    def test_to_dict_is_extended_by_children(self):
        self.assertIn("blood_group", make_patient().to_dict())
        self.assertIn("license_number", make_doctor().to_dict())
        self.assertNotIn("license_number", make_patient().to_dict())


class EncapsulationTests(unittest.TestCase):
    def test_private_attribute_is_not_directly_visible(self):
        patient = make_patient()
        self.assertFalse(hasattr(patient, "first_name_value"))
        self.assertFalse(hasattr(patient, "__first_name"))

    def test_setter_validates(self):
        patient = make_patient()
        with self.assertRaises(ValidationError):
            patient.phone = "bad"
        with self.assertRaises(ValidationError):
            patient.blood_group = "Z+"
        patient.phone = "0782223333"
        self.assertEqual(patient.phone, "0782223333")

    def test_constructor_validates(self):
        with self.assertRaises(ValidationError):
            make_patient(national_id="nope")
        with self.assertRaises(ValidationError):
            make_doctor(license_number="!")

    def test_id_must_be_positive_int(self):
        patient = make_patient()
        with self.assertRaises(ValidationError):
            patient.id = 0
        patient.id = 5
        self.assertEqual(patient.id, 5)

    def test_age_is_calculated(self):
        patient = make_patient(date_of_birth="2000-01-01")
        self.assertGreaterEqual(patient.age, 25)

    def test_describe_handles_missing_optional_fields(self):
        patient = make_patient(email="", address="", allergies="",
                               emergency_contact_name="", emergency_contact_phone="")
        text = patient.describe()
        self.assertIn("not provided", text)
        self.assertIn("none recorded", text)


if __name__ == "__main__":
    unittest.main()
