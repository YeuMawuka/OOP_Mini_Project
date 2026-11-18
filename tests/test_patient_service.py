import unittest

from services.base_service import BaseService
from services.patient_service import PatientService
from tests.helpers import make_database, make_patient
from utils.exceptions import DuplicateError, NotFoundError, ValidationError


class PatientServiceTests(unittest.TestCase):
    def setUp(self):
        self.db = make_database()
        self.service = PatientService(self.db)

    def tearDown(self):
        self.db.close()

    def test_service_extends_abstract_base(self):
        self.assertIsInstance(self.service, BaseService)
        with self.assertRaises(TypeError):
            BaseService(self.db)

    def test_create_assigns_id_and_get_by_id_returns_patient(self):
        patient = self.service.create(make_patient())
        self.assertEqual(patient.id, 1)
        loaded = self.service.get_by_id(1)
        self.assertEqual(loaded.full_name, "Tendai Moyo")
        self.assertEqual(loaded.blood_group, "O+")

    def test_duplicate_national_id_is_rejected(self):
        self.service.create(make_patient())
        with self.assertRaises(DuplicateError):
            self.service.create(make_patient(first_name="Other"))

    def test_search_by_name_id_and_phone(self):
        self.service.create(make_patient())
        self.service.create(make_patient(first_name="Chipo", last_name="Dube",
                                         national_id="63-222222-B-42", phone="0772223333"))
        self.assertEqual(len(self.service.search("moyo")), 1)
        self.assertEqual(len(self.service.search("Chipo Dube")), 1)
        self.assertEqual(len(self.service.search("222222")), 1)
        self.assertEqual(len(self.service.search("0772")), 1)
        self.assertEqual(self.service.search("zzz"), [])

    def test_search_requires_keyword(self):
        with self.assertRaises(ValidationError):
            self.service.search("   ")

    def test_update_saves_changes(self):
        patient = self.service.create(make_patient())
        patient.phone = "0783334444"
        patient.allergies = "None"
        self.service.update(patient)
        loaded = self.service.get_by_id(patient.id)
        self.assertEqual(loaded.phone, "0783334444")
        self.assertEqual(loaded.allergies, "None")

    def test_update_cannot_reuse_another_national_id(self):
        self.service.create(make_patient())
        second = self.service.create(make_patient(national_id="63-222222-B-42"))
        second.national_id = "63-123456-A-42"
        with self.assertRaises(DuplicateError):
            self.service.update(second)

    def test_update_of_unsaved_patient_fails(self):
        from utils.exceptions import BusinessRuleError
        with self.assertRaises(BusinessRuleError):
            self.service.update(make_patient())

    def test_delete_removes_patient(self):
        patient = self.service.create(make_patient())
        self.service.delete(patient.id)
        self.assertEqual(self.service.count(), 0)
        with self.assertRaises(NotFoundError):
            self.service.get_by_id(patient.id)

    def test_delete_missing_patient_raises(self):
        with self.assertRaises(NotFoundError):
            self.service.delete(42)

    def test_list_all_and_count(self):
        self.service.create(make_patient())
        self.service.create(make_patient(national_id="63-222222-B-42"))
        self.assertEqual(self.service.count(), 2)
        self.assertEqual([p.id for p in self.service.list_all()], [1, 2])


if __name__ == "__main__":
    unittest.main()
