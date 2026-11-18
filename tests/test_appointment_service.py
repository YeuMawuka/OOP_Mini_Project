import unittest

from services.appointment_service import AppointmentService
from services.doctor_service import DoctorService
from services.patient_service import PatientService
from tests.helpers import make_appointment, make_database, make_doctor, make_patient
from utils.exceptions import BusinessRuleError, NotFoundError, ValidationError


class AppointmentServiceTests(unittest.TestCase):
    def setUp(self):
        self.db = make_database()
        self.patients = PatientService(self.db)
        self.doctors = DoctorService(self.db)
        self.service = AppointmentService(self.db)
        self.patients.create(make_patient())
        self.doctors.create(make_doctor())

    def tearDown(self):
        self.db.close()

    def test_create_and_get(self):
        appointment = self.service.create(make_appointment())
        loaded = self.service.get_by_id(appointment.id)
        self.assertEqual(loaded.appointment_date, "2026-12-01")
        self.assertEqual(loaded.status, "Scheduled")

    def test_unknown_patient_or_doctor_is_rejected(self):
        with self.assertRaises(NotFoundError):
            self.service.create(make_appointment(patient_id=99))
        with self.assertRaises(NotFoundError):
            self.service.create(make_appointment(doctor_id=99))

    def test_double_booking_is_rejected(self):
        self.service.create(make_appointment())
        with self.assertRaises(BusinessRuleError):
            self.service.create(make_appointment(reason="Another visit"))

    def test_different_time_is_allowed(self):
        self.service.create(make_appointment())
        self.service.create(make_appointment(appointment_time="10:30"))
        self.assertEqual(self.service.count(), 2)

    def test_update_changes_fields(self):
        appointment = self.service.create(make_appointment())
        appointment.appointment_time = "11:00"
        appointment.reason = "Follow-up"
        self.service.update(appointment)
        loaded = self.service.get_by_id(appointment.id)
        self.assertEqual(loaded.appointment_time, "11:00")
        self.assertEqual(loaded.reason, "Follow-up")

    def test_update_to_taken_slot_is_rejected(self):
        self.service.create(make_appointment())
        second = self.service.create(make_appointment(appointment_time="10:30"))
        second.appointment_time = "09:30"
        with self.assertRaises(BusinessRuleError):
            self.service.update(second)

    def test_update_keeping_own_slot_is_allowed(self):
        appointment = self.service.create(make_appointment())
        appointment.reason = "Updated reason"
        self.service.update(appointment)
        self.assertEqual(self.service.get_by_id(appointment.id).reason, "Updated reason")

    def test_cancel_keeps_row_and_frees_slot(self):
        appointment = self.service.create(make_appointment())
        self.service.cancel(appointment.id)
        self.assertEqual(self.service.get_by_id(appointment.id).status, "Cancelled")
        self.service.create(make_appointment())
        self.assertEqual(self.service.count(), 2)

    def test_cancel_twice_is_rejected(self):
        appointment = self.service.create(make_appointment())
        self.service.cancel(appointment.id)
        with self.assertRaises(BusinessRuleError):
            self.service.cancel(appointment.id)

    def test_cancel_missing_appointment(self):
        with self.assertRaises(NotFoundError):
            self.service.cancel(77)

    def test_list_details_filters(self):
        self.patients.create(make_patient(national_id="63-222222-B-42", first_name="Chipo"))
        self.service.create(make_appointment())
        self.service.create(make_appointment(patient_id=2, appointment_time="10:00"))
        self.assertEqual(len(self.service.list_details()), 2)
        self.assertEqual(len(self.service.list_details(patient_id=2)), 1)
        self.assertEqual(len(self.service.list_details(doctor_id=1)), 2)
        self.service.cancel(1)
        self.assertEqual(len(self.service.list_details(status="cancelled")), 1)
        first = self.service.list_details(patient_id=1)[0]
        self.assertEqual(first["patient_name"], "Tendai Moyo")
        self.assertEqual(first["doctor_name"], "Farai Chikwanha")

    def test_list_details_rejects_bad_status(self):
        with self.assertRaises(ValidationError):
            self.service.list_details(status="Pending")

    def test_count_by_status(self):
        self.service.create(make_appointment())
        second = self.service.create(make_appointment(appointment_time="10:30"))
        self.service.cancel(second.id)
        self.assertEqual(self.service.count_by_status(),
                         {"Scheduled": 1, "Completed": 0, "Cancelled": 1})

    def test_search(self):
        self.service.create(make_appointment())
        self.assertEqual(len(self.service.search("chest")), 1)
        self.assertEqual(len(self.service.search("2026-12")), 1)
        self.assertEqual(self.service.search("nothing"), [])

    def test_doctor_with_appointments_cannot_be_deleted(self):
        self.service.create(make_appointment())
        with self.assertRaises(BusinessRuleError):
            self.doctors.delete(1)
        self.assertEqual(self.doctors.count(), 1)

    def test_deleting_patient_removes_their_appointments(self):
        self.service.create(make_appointment())
        self.patients.delete(1)
        self.assertEqual(self.service.count(), 0)


if __name__ == "__main__":
    unittest.main()
