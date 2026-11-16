import unittest

from models.appointment import Appointment
from models.base_entity import BaseEntity
from models.medical_record import MedicalRecord
from tests.helpers import make_appointment, make_record
from utils.exceptions import BusinessRuleError, ValidationError


class AppointmentModelTests(unittest.TestCase):
    def test_is_a_base_entity(self):
        self.assertTrue(issubclass(Appointment, BaseEntity))

    def test_defaults_to_scheduled(self):
        self.assertEqual(make_appointment().status, "Scheduled")

    def test_cancel_changes_status(self):
        appointment = make_appointment()
        appointment.cancel()
        self.assertEqual(appointment.status, "Cancelled")

    def test_cancel_twice_is_rejected(self):
        appointment = make_appointment()
        appointment.cancel()
        with self.assertRaises(BusinessRuleError):
            appointment.cancel()

    def test_completed_cannot_be_cancelled(self):
        appointment = make_appointment(status="Completed")
        with self.assertRaises(BusinessRuleError):
            appointment.cancel()

    def test_setters_validate(self):
        appointment = make_appointment()
        with self.assertRaises(ValidationError):
            appointment.appointment_time = "99:99"
        with self.assertRaises(ValidationError):
            appointment.status = "Pending"
        with self.assertRaises(ValidationError):
            appointment.patient_id = 0

    def test_describe_and_to_dict(self):
        appointment = make_appointment(entity_id=3)
        self.assertIn("Appointment #3", appointment.describe())
        self.assertEqual(appointment.to_dict()["appointment_time"], "09:30")


class MedicalRecordModelTests(unittest.TestCase):
    def test_is_a_base_entity(self):
        self.assertTrue(issubclass(MedicalRecord, BaseEntity))

    def test_appointment_is_optional(self):
        self.assertIsNone(make_record().appointment_id)
        self.assertEqual(make_record(appointment_id=4).appointment_id, 4)

    def test_required_fields_are_validated(self):
        with self.assertRaises(ValidationError):
            make_record(diagnosis="")
        with self.assertRaises(ValidationError):
            make_record(visit_date="yesterday")

    def test_optional_fields_may_be_blank(self):
        record = make_record(prescription="", notes="")
        self.assertIn("Prescription : none", record.describe())

    def test_describe_and_to_dict_override(self):
        record = make_record(entity_id=2)
        self.assertIn("Medical record #2", record.describe())
        self.assertEqual(record.to_dict()["diagnosis"], "Hypertension")


if __name__ == "__main__":
    unittest.main()
