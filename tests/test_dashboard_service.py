import unittest

from services.appointment_service import AppointmentService
from services.dashboard_service import DashboardService
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


class DashboardServiceTests(unittest.TestCase):
    def setUp(self):
        self.db = make_database()
        self.patients = PatientService(self.db)
        self.doctors = DoctorService(self.db)
        self.appointments = AppointmentService(self.db)
        self.records = MedicalRecordService(self.db)
        self.dashboard = DashboardService(
            self.patients, self.doctors, self.appointments, self.records)

    def tearDown(self):
        self.db.close()

    def test_empty_system_has_zero_totals(self):
        summary = self.dashboard.get_summary()
        self.assertEqual(summary["total_patients"], 0)
        self.assertEqual(summary["total_doctors"], 0)
        self.assertEqual(summary["total_appointments"], 0)
        self.assertEqual(summary["total_medical_records"], 0)

    def test_totals_follow_the_data(self):
        self.patients.create(make_patient())
        self.doctors.create(make_doctor())
        self.appointments.create(make_appointment())
        self.records.create(make_record())
        summary = self.dashboard.get_summary()
        self.assertEqual(summary["total_patients"], 1)
        self.assertEqual(summary["total_doctors"], 1)
        self.assertEqual(summary["total_appointments"], 1)
        self.assertEqual(summary["total_medical_records"], 1)
        self.assertEqual(summary["appointments_by_status"]["Scheduled"], 1)

    def test_render_contains_every_total(self):
        text = self.dashboard.render()
        for label in ("Total patients", "Total doctors", "Total appointments",
                      "Total medical records", "Scheduled", "Cancelled"):
            self.assertIn(label, text)


if __name__ == "__main__":
    unittest.main()
