"""Custom exception hierarchy for the EHR Management System.

Every error that the system raises on purpose inherits from EHRError, so the
menu layer can catch one base class and show a friendly message instead of
crashing with a traceback.
"""


class EHRError(Exception):
    """Base class for every deliberate error raised by the EHR system."""


class ValidationError(EHRError):
    """Raised when a value typed by the user (or passed to a class) is invalid."""


class NotFoundError(EHRError):
    """Raised when a record with the requested ID does not exist."""


class DuplicateError(EHRError):
    """Raised when a unique value (such as a National ID) is already in use."""


class BusinessRuleError(EHRError):
    """Raised when an action breaks a business rule of the hospital workflow."""
