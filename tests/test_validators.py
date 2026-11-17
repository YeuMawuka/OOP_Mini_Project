import unittest
from datetime import date, timedelta

from utils.exceptions import ValidationError
from utils.validators import Validators


class ValidatorTests(unittest.TestCase):
    def test_text_trims_and_requires_value(self):
        self.assertEqual(Validators.text("  hello  ", "Field"), "hello")
        with self.assertRaises(ValidationError):
            Validators.text("   ", "Field")

    def test_text_optional_returns_empty_string(self):
        self.assertEqual(Validators.text("", "Field", required=False), "")

    def test_text_rejects_too_long_value(self):
        with self.assertRaises(ValidationError):
            Validators.text("x" * 11, "Field", max_length=10)

    def test_name_accepts_hyphen_and_apostrophe(self):
        self.assertEqual(Validators.name("Mary-Anne O'Neil", "Name"), "Mary-Anne O'Neil")

    def test_name_rejects_digits(self):
        with self.assertRaises(ValidationError):
            Validators.name("John3", "Name")

    def test_national_id_is_normalised(self):
        self.assertEqual(Validators.national_id("63123456a42"), "63-123456-A-42")
        self.assertEqual(Validators.national_id("63-1234567-b-05"), "63-1234567-B-05")

    def test_national_id_rejects_bad_format(self):
        for bad in ("123", "63-12-A-42", "ABCDEFGHIJ"):
            with self.assertRaises(ValidationError):
                Validators.national_id(bad)

    def test_phone_accepts_local_and_international(self):
        self.assertEqual(Validators.phone("077 123 4567"), "0771234567")
        self.assertEqual(Validators.phone("+263 77 123 4567"), "+263771234567")

    def test_phone_rejects_bad_number(self):
        with self.assertRaises(ValidationError):
            Validators.phone("12345")

    def test_phone_optional_blank(self):
        self.assertEqual(Validators.phone("", required=False), "")

    def test_email_valid_invalid_and_optional(self):
        self.assertEqual(Validators.email("USER@Example.com"), "user@example.com")
        self.assertEqual(Validators.email(""), "")
        with self.assertRaises(ValidationError):
            Validators.email("not-an-email")

    def test_date_value_normalises(self):
        self.assertEqual(Validators.date_value("2026-1-5"), "2026-01-05")

    def test_date_value_rejects_impossible_date(self):
        with self.assertRaises(ValidationError):
            Validators.date_value("2026-02-30")

    def test_date_of_birth_rejects_future_and_ancient(self):
        future = (date.today() + timedelta(days=2)).isoformat()
        with self.assertRaises(ValidationError):
            Validators.date_of_birth(future)
        with self.assertRaises(ValidationError):
            Validators.date_of_birth("1800-01-01")

    def test_time_value(self):
        self.assertEqual(Validators.time_value("9:05"), "09:05")
        with self.assertRaises(ValidationError):
            Validators.time_value("25:00")

    def test_choice_ignores_case(self):
        self.assertEqual(Validators.choice("female", Validators.GENDERS, "Gender"), "Female")
        with self.assertRaises(ValidationError):
            Validators.choice("robot", Validators.GENDERS, "Gender")

    def test_positive_int(self):
        self.assertEqual(Validators.positive_int("7"), 7)
        for bad in ("0", "-3", "abc"):
            with self.assertRaises(ValidationError):
                Validators.positive_int(bad)

    def test_license_number_is_upper_cased(self):
        self.assertEqual(Validators.license_number("mdpcz-10234"), "MDPCZ-10234")
        with self.assertRaises(ValidationError):
            Validators.license_number("a")


if __name__ == "__main__":
    unittest.main()
