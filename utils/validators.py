"""Input validation utilities.

All checks live in the Validators class so that the entity classes and the
menu layer share exactly the same rules. Every method returns the cleaned
(normalised) value or raises ValidationError.
"""

import re
from datetime import date, datetime

from utils.exceptions import ValidationError


class Validators:
    """Collection of static validation helpers (a utility class)."""

    GENDERS = ("Male", "Female", "Other")
    BLOOD_GROUPS = ("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown")
    PROVINCES = (
        "Bulawayo",
        "Harare",
        "Manicaland",
        "Mashonaland Central",
        "Mashonaland East",
        "Mashonaland West",
        "Masvingo",
        "Matabeleland North",
        "Matabeleland South",
        "Midlands",
    )
    APPOINTMENT_STATUSES = ("Scheduled", "Completed", "Cancelled")

    _NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z' \-]*$")
    _NATIONAL_ID_PATTERN = re.compile(r"^(\d{2})(\d{6,7})([A-Z])(\d{2})$")
    _PHONE_PATTERN = re.compile(r"^(\+263|0)\d{9}$")
    _EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    _LICENSE_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9\-/]{2,19}$")

    @staticmethod
    def text(value, field, max_length=255, required=True):
        """Trim a text value and check that it is present and not too long."""
        cleaned = "" if value is None else str(value).strip()
        if not cleaned:
            if required:
                raise ValidationError(f"{field} is required.")
            return ""
        if len(cleaned) > max_length:
            raise ValidationError(f"{field} must not be longer than {max_length} characters.")
        return cleaned

    @staticmethod
    def name(value, field="Name", required=True):
        """Validate a personal name (letters, spaces, hyphens, apostrophes)."""
        cleaned = Validators.text(value, field, 50, required)
        if not cleaned:
            return ""
        if not Validators._NAME_PATTERN.match(cleaned):
            raise ValidationError(f"{field} may only contain letters, spaces, hyphens and apostrophes.")
        return cleaned

    @staticmethod
    def national_id(value):
        """Validate a Zimbabwean National ID such as 63-123456-A-42."""
        cleaned = Validators.text(value, "National ID", 20)
        compact = cleaned.replace("-", "").replace(" ", "").upper()
        match = Validators._NATIONAL_ID_PATTERN.match(compact)
        if not match:
            raise ValidationError("National ID must look like 63-123456-A-42.")
        return "-".join(match.groups())

    @staticmethod
    def phone(value, field="Phone number", required=True):
        """Validate a Zimbabwean phone number (+263771234567 or 0771234567)."""
        cleaned = Validators.text(value, field, 30, required)
        if not cleaned:
            return ""
        compact = re.sub(r"[\s\-()]", "", cleaned)
        if not Validators._PHONE_PATTERN.match(compact):
            raise ValidationError(f"{field} must look like +263771234567 or 0771234567.")
        return compact

    @staticmethod
    def email(value, required=False):
        """Validate an optional e-mail address."""
        cleaned = Validators.text(value, "Email", 100, required)
        if not cleaned:
            return ""
        if not Validators._EMAIL_PATTERN.match(cleaned):
            raise ValidationError("Email must look like name@example.com.")
        return cleaned.lower()

    @staticmethod
    def date_value(value, field="Date"):
        """Validate a calendar date typed as YYYY-MM-DD and return it normalised."""
        cleaned = Validators.text(value, field, 10)
        try:
            return datetime.strptime(cleaned, "%Y-%m-%d").date().isoformat()
        except ValueError:
            raise ValidationError(f"{field} must be a real date in the form YYYY-MM-DD.")

    @staticmethod
    def date_of_birth(value):
        """Validate a date of birth: a real date, not in the future, not absurdly old."""
        iso = Validators.date_value(value, "Date of birth")
        born = date.fromisoformat(iso)
        today = date.today()
        if born > today:
            raise ValidationError("Date of birth cannot be in the future.")
        if born.year < today.year - 130:
            raise ValidationError("Date of birth is too far in the past.")
        return iso

    @staticmethod
    def time_value(value, field="Time"):
        """Validate a 24-hour clock time typed as HH:MM and return it normalised."""
        cleaned = Validators.text(value, field, 5)
        try:
            return datetime.strptime(cleaned, "%H:%M").strftime("%H:%M")
        except ValueError:
            raise ValidationError(f"{field} must be a 24-hour time in the form HH:MM.")

    @staticmethod
    def choice(value, options, field):
        """Match a value against allowed options, ignoring letter case."""
        cleaned = Validators.text(value, field, 50)
        for option in options:
            if option.lower() == cleaned.lower():
                return option
        raise ValidationError(f"{field} must be one of: {', '.join(options)}.")

    @staticmethod
    def positive_int(value, field="ID"):
        """Validate a positive whole number (used for record IDs)."""
        try:
            number = int(str(value).strip())
        except ValueError:
            raise ValidationError(f"{field} must be a whole number.")
        if number <= 0:
            raise ValidationError(f"{field} must be greater than zero.")
        return number

    @staticmethod
    def license_number(value):
        """Validate a medical practitioner registration number (e.g. MDPCZ-10234)."""
        cleaned = Validators.text(value, "License number", 20).upper()
        if not Validators._LICENSE_PATTERN.match(cleaned):
            raise ValidationError(
                "License number must be 3-20 characters: letters, digits, '-' or '/'."
            )
        return cleaned
