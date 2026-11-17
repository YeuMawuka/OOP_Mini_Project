import sqlite3
import unittest

from tests.helpers import make_database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.db = make_database()

    def tearDown(self):
        self.db.close()

    def test_people_tables_are_created(self):
        rows = self.db.fetch_all("SELECT name FROM sqlite_master WHERE type = 'table'")
        names = {row["name"] for row in rows}
        self.assertIn("patients", names)
        self.assertIn("doctors", names)

    def test_check_constraint_rejects_bad_gender(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute(
                "INSERT INTO patients (first_name, last_name, national_id, date_of_birth, "
                "gender, phone, province) VALUES ('A', 'B', '63-123456-A-42', '1990-01-01', "
                "'Robot', '0771234567', 'Harare')"
            )

    def test_unique_national_id_is_enforced(self):
        sql = (
            "INSERT INTO patients (first_name, last_name, national_id, date_of_birth, "
            "gender, phone, province) VALUES ('A', 'B', '63-123456-A-42', '1990-01-01', "
            "'Male', '0771234567', 'Harare')"
        )
        self.db.execute(sql)
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute(sql)

    def test_failed_statement_is_rolled_back(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute(
                "INSERT INTO patients (first_name, last_name, national_id, date_of_birth, "
                "gender, phone, province) VALUES ('A', 'B', '63-123456-A-42', '1990-01-01', "
                "'Robot', '0771234567', 'Harare')"
            )
        self.assertEqual(self.db.scalar("SELECT COUNT(*) FROM patients"), 0)

    def test_scalar_and_fetch_helpers(self):
        self.assertEqual(self.db.scalar("SELECT COUNT(*) FROM patients"), 0)
        self.assertIsNone(self.db.fetch_one("SELECT * FROM patients"))
        self.assertEqual(self.db.fetch_all("SELECT * FROM patients"), [])

    def test_context_manager_closes_connection(self):
        from database.connection import Database
        with Database(":memory:") as database:
            self.assertEqual(database.path, ":memory:")
        with self.assertRaises(sqlite3.ProgrammingError):
            database.scalar("SELECT 1")


if __name__ == "__main__":
    unittest.main()
