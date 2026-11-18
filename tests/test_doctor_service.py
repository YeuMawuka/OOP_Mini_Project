import unittest

from services.doctor_service import DoctorService
from tests.helpers import make_database, make_doctor
from utils.exceptions import DuplicateError, NotFoundError


class DoctorServiceTests(unittest.TestCase):
    def setUp(self):
        self.db = make_database()
        self.service = DoctorService(self.db)

    def tearDown(self):
        self.db.close()

    def test_create_and_get(self):
        doctor = self.service.create(make_doctor())
        loaded = self.service.get_by_id(doctor.id)
        self.assertEqual(loaded.license_number, "MDPCZ-10234")
        self.assertEqual(loaded.get_role(), "Doctor")

    def test_duplicate_national_id_and_license_rejected(self):
        self.service.create(make_doctor())
        with self.assertRaises(DuplicateError):
            self.service.create(make_doctor(license_number="MDPCZ-99999"))
        with self.assertRaises(DuplicateError):
            self.service.create(make_doctor(national_id="08-111111-C-12"))

    def test_search_by_specialization_and_license(self):
        self.service.create(make_doctor())
        self.service.create(make_doctor(first_name="Nyasha", national_id="08-222222-D-12",
                                        license_number="MDPCZ-20000",
                                        specialization="Paediatrics", department="Children"))
        self.assertEqual(len(self.service.search("cardio")), 1)
        self.assertEqual(len(self.service.search("MDPCZ-2")), 1)
        self.assertEqual(len(self.service.search("chikwanha")), 2)

    def test_update(self):
        doctor = self.service.create(make_doctor())
        doctor.department = "Emergency"
        self.service.update(doctor)
        self.assertEqual(self.service.get_by_id(doctor.id).department, "Emergency")

    def test_update_cannot_reuse_license(self):
        self.service.create(make_doctor())
        second = self.service.create(make_doctor(national_id="08-222222-D-12",
                                                 license_number="MDPCZ-20000"))
        second.license_number = "MDPCZ-10234"
        with self.assertRaises(DuplicateError):
            self.service.update(second)

    def test_delete(self):
        doctor = self.service.create(make_doctor())
        self.service.delete(doctor.id)
        with self.assertRaises(NotFoundError):
            self.service.get_by_id(doctor.id)


if __name__ == "__main__":
    unittest.main()
