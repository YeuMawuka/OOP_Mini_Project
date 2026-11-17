import os
import tempfile
import unittest

from database.connection import Database
from services.appointment_service import AppointmentService
from services.doctor_service import DoctorService
from services.medical_record_service import MedicalRecordService
from services.patient_service import PatientService
from tests.helpers import (
    make_appointment,
    make_doctor,
    make_patient,
    make_record,
)


class PersistenceTests(unittest.TestCase):
    def test_records_survive_closing_and_reopening(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "nested", "ehr.db")

            first = Database(path)
            PatientService(first).create(make_patient())
            DoctorService(first).create(make_doctor())
            AppointmentService(first).create(make_appointment())
            MedicalRecordService(first).create(make_record())
            first.close()
            self.assertTrue(os.path.exists(path))

            second = Database(path)
            self.assertEqual(PatientService(second).count(), 1)
            self.assertEqual(DoctorService(second).count(), 1)
            self.assertEqual(AppointmentService(second).count(), 1)
            self.assertEqual(MedicalRecordService(second).count(), 1)
            self.assertEqual(PatientService(second).get_by_id(1).full_name, "Tendai Moyo")
            second.close()


if __name__ == "__main__":
    unittest.main()
