import unittest

from services.appointment_service import AppointmentService
from services.doctor_service import DoctorService
from services.medical_record_service import MedicalRecordService
from services.patient_service import PatientService
from tests.helpers import (
    make_appointment,
    make_database,
    make_doctor,
    make_patient,
    make_record,
)
from utils.exceptions import BusinessRuleError, NotFoundError


class MedicalRecordServiceTests(unittest.TestCase):
    def setUp(self):
        self.db = make_database()
        self.patients = PatientService(self.db)
        self.doctors = DoctorService(self.db)
        self.appointments = AppointmentService(self.db)
        self.service = MedicalRecordService(self.db)
        self.patients.create(make_patient())
        self.doctors.create(make_doctor())

    def tearDown(self):
        self.db.close()

    def test_create_and_get(self):
        record = self.service.create(make_record())
        loaded = self.service.get_by_id(record.id)
        self.assertEqual(loaded.diagnosis, "Hypertension")
        self.assertIsNone(loaded.appointment_id)

    def test_unknown_patient_or_doctor_rejected(self):
        with self.assertRaises(NotFoundError):
            self.service.create(make_record(patient_id=9))
        with self.assertRaises(NotFoundError):
            self.service.create(make_record(doctor_id=9))

    def test_linking_scheduled_appointment_completes_it(self):
        appointment = self.appointments.create(make_appointment())
        self.service.create(make_record(appointment_id=appointment.id))
        self.assertEqual(self.appointments.get_by_id(appointment.id).status, "Completed")

    def test_unknown_appointment_rejected(self):
        with self.assertRaises(NotFoundError):
            self.service.create(make_record(appointment_id=50))

    def test_cancelled_appointment_rejected(self):
        appointment = self.appointments.create(make_appointment())
        self.appointments.cancel(appointment.id)
        with self.assertRaises(BusinessRuleError):
            self.service.create(make_record(appointment_id=appointment.id))

    def test_appointment_of_other_patient_rejected(self):
        self.patients.create(make_patient(national_id="63-222222-B-42"))
        appointment = self.appointments.create(make_appointment(patient_id=2))
        with self.assertRaises(BusinessRuleError):
            self.service.create(make_record(patient_id=1, appointment_id=appointment.id))

    def test_history_is_newest_first(self):
        self.service.create(make_record(visit_date="2026-01-10", diagnosis="Flu"))
        self.service.create(make_record(visit_date="2026-06-10", diagnosis="Malaria"))
        history = self.service.get_history(1)
        self.assertEqual([r.diagnosis for r in history], ["Malaria", "Flu"])

    def test_history_details_include_doctor_name(self):
        self.service.create(make_record())
        details = self.service.get_history_details(1)
        self.assertEqual(details[0]["doctor_name"], "Farai Chikwanha")

    def test_history_of_unknown_patient(self):
        with self.assertRaises(NotFoundError):
            self.service.get_history(99)
        with self.assertRaises(NotFoundError):
            self.service.get_history_details(99)

    def test_history_only_contains_that_patient(self):
        self.patients.create(make_patient(national_id="63-222222-B-42"))
        self.service.create(make_record(patient_id=1))
        self.service.create(make_record(patient_id=2))
        self.assertEqual(len(self.service.get_history(1)), 1)

    def test_update_record(self):
        record = self.service.create(make_record())
        record.diagnosis = "Controlled hypertension"
        record.notes = "Stable"
        self.service.update(record)
        loaded = self.service.get_by_id(record.id)
        self.assertEqual(loaded.diagnosis, "Controlled hypertension")
        self.assertEqual(loaded.notes, "Stable")

    def test_update_missing_record(self):
        record = make_record(entity_id=99)
        with self.assertRaises(NotFoundError):
            self.service.update(record)

    def test_search(self):
        self.service.create(make_record())
        self.assertEqual(len(self.service.search("amlodipine")), 1)
        self.assertEqual(len(self.service.search("hyper")), 1)
        self.assertEqual(self.service.search("xyz"), [])

    def test_deleting_patient_removes_records(self):
        self.service.create(make_record())
        self.patients.delete(1)
        self.assertEqual(self.service.count(), 0)

    def test_deleting_appointment_keeps_record(self):
        appointment = self.appointments.create(make_appointment())
        record = self.service.create(make_record(appointment_id=appointment.id))
        self.appointments.delete(appointment.id)
        self.assertIsNone(self.service.get_by_id(record.id).appointment_id)


if __name__ == "__main__":
    unittest.main()
