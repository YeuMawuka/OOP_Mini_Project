import sqlite3
import unittest

from tests.helpers import make_database


class SchemaRelationshipTests(unittest.TestCase):
    def setUp(self):
        self.db = make_database()

    def tearDown(self):
        self.db.close()

    def test_all_four_tables_exist(self):
        rows = self.db.fetch_all("SELECT name FROM sqlite_master WHERE type = 'table'")
        names = {row["name"] for row in rows}
        for table in ("patients", "doctors", "appointments", "medical_records"):
            self.assertIn(table, names)

    def test_foreign_keys_are_switched_on(self):
        self.assertEqual(self.db.scalar("PRAGMA foreign_keys"), 1)

    def test_appointment_needs_existing_patient_and_doctor(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute(
                "INSERT INTO appointments (patient_id, doctor_id, appointment_date, "
                "appointment_time, reason) VALUES (99, 99, '2026-12-01', '09:00', 'x')"
            )

    def test_medical_record_needs_existing_patient_and_doctor(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute(
                "INSERT INTO medical_records (patient_id, doctor_id, visit_date, "
                "diagnosis, treatment) VALUES (99, 99, '2026-12-01', 'x', 'y')"
            )

    def test_appointment_status_check_constraint(self):
        from tests.helpers import make_doctor, make_patient
        from services.doctor_service import DoctorService
        from services.patient_service import PatientService
        PatientService(self.db).create(make_patient())
        DoctorService(self.db).create(make_doctor())
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute(
                "INSERT INTO appointments (patient_id, doctor_id, appointment_date, "
                "appointment_time, reason, status) VALUES (1, 1, '2026-12-01', '09:00', "
                "'x', 'Pending')"
            )


if __name__ == "__main__":
    unittest.main()
