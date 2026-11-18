import unittest

from main import build_application
from tests.helpers import make_database
from ui.console import Console


class ScriptedInput:
    """Feeds prepared answers to the console, like a person typing."""

    def __init__(self, answers):
        self._answers = list(answers)

    def __call__(self, prompt=""):
        if not self._answers:
            raise EOFError("script finished")
        return self._answers.pop(0)


def run_script(answers, database=None):
    database = database or make_database()
    output = []
    console = Console(ScriptedInput(answers), output.append)
    try:
        build_application(database, console).run()
    except EOFError:
        pass
    return "\n".join(str(line) for line in output), database


PATIENT_ANSWERS = [
    "Tendai", "Moyo", "63-123456-A-42", "1990-05-17", "female", "0771234567", "",
    "12 Samora Machel Avenue", "", "o+", "Penicillin", "Rudo Moyo", "0712345678",
]
DOCTOR_ANSWERS = [
    "Farai", "Chikwanha", "08-765432-B-12", "1980-03-02", "Male", "+263772000111",
    "f.chikwanha@example.co.zw", "Cardiology", "MDPCZ-10234", "Cardiology",
]


class MenuTests(unittest.TestCase):
    def test_full_workflow_through_the_menus(self):
        answers = (
            ["2", "1"] + DOCTOR_ANSWERS + ["0"]
            + ["1", "1"] + PATIENT_ANSWERS + ["0"]
            + ["3", "1", "1", "1", "2026-12-01", "09:30", "Headache follow-up", "0"]
            + ["4", "1", "1", "1", "1", "2026-12-01", "Migraine", "Rest and fluids",
               "Paracetamol 500mg", "", "2", "1", "0"]
            + ["5", "0"]
        )
        output, database = run_script(answers)
        self.assertIn("Doctor registered with ID 1", output)
        self.assertIn("Patient registered with ID 1", output)
        self.assertIn("Appointment created with ID 1", output)
        self.assertIn("Medical record created with ID 1", output)
        self.assertIn("Medical history for patient 1: 1 record(s)", output)
        self.assertIn("Migraine", output)
        self.assertIn("Total patients        : 1", output)
        self.assertIn("Completed : 1", output)
        database.close()

    def test_validation_errors_are_retried(self):
        answers = ["1", "1", "Tendai", "Moyo", "bad-id", "63-123456-A-42", "1990-05-17",
                   "female", "0771234567", "", "", "", "", "", "", "", "0", "0"]
        output, database = run_script(answers)
        self.assertIn("Invalid input", output)
        self.assertIn("Patient registered with ID 1", output)
        database.close()

    def test_service_errors_are_shown_not_raised(self):
        answers = ["1", "3", "99", "0", "0"]
        output, database = run_script(answers)
        self.assertIn("Error: No patient found with ID 99.", output)
        database.close()

    def test_invalid_menu_option(self):
        output, database = run_script(["9", "abc", "0"])
        self.assertEqual(output.count("Invalid option"), 2)
        database.close()

    def test_search_update_and_delete_patient(self):
        answers = (
            ["1", "1"] + PATIENT_ANSWERS
            + ["2", "moyo"]
            + ["3", "1"] + [""] * 13
            + ["5", "1"]
            + ["6"]
            + ["4", "1", "n"]
            + ["4", "1", "y"]
            + ["6", "0", "0"]
        )
        output, database = run_script(answers)
        self.assertIn("Tendai Moyo", output)
        self.assertIn("Patient updated.", output)
        self.assertIn("Deletion cancelled.", output)
        self.assertIn("Patient deleted.", output)
        self.assertIn("(no records found)", output)
        database.close()

    def test_doctor_search_update_view_delete(self):
        answers = (
            ["2", "1"] + DOCTOR_ANSWERS
            + ["2", "cardio"]
            + ["3", "1"] + [""] * 10
            + ["5", "1"]
            + ["6"]
            + ["4", "1", "y"]
            + ["0", "0"]
        )
        output, database = run_script(answers)
        self.assertIn("Doctor updated.", output)
        self.assertIn("Dr. Farai Chikwanha", output)
        self.assertIn("Doctor deleted.", output)
        database.close()

    def test_appointment_update_cancel_and_view_filters(self):
        def appointments(*steps):
            return ["3"] + list(steps) + ["0"]

        answers = (
            ["2", "1"] + DOCTOR_ANSWERS + ["0"]
            + ["1", "1"] + PATIENT_ANSWERS + ["0"]
            + appointments("1", "1", "1", "2026-12-01", "09:30", "Headache")
            + appointments("2", "1", "", "", "11:15", "", "")
            + appointments("3", "1", "n")
            + appointments("3", "1", "y")
            + appointments("3", "1", "y")
            + appointments("4", "1")
            + appointments("4", "2", "1")
            + appointments("4", "3", "1")
            + appointments("4", "4", "cancelled")
        )
        output, database = run_script(answers)
        self.assertIn("Appointment updated.", output)
        self.assertIn("11:15", output)
        self.assertIn("Cancellation aborted.", output)
        self.assertIn("Appointment cancelled.", output)
        self.assertIn("Error: This appointment is already cancelled.", output)
        self.assertIn("Cancelled", output)
        database.close()

    def test_medical_record_update_and_view_one(self):
        answers = (
            ["2", "1"] + DOCTOR_ANSWERS + ["0"]
            + ["1", "1"] + PATIENT_ANSWERS + ["0"]
            + ["4", "1", "1", "1", "", "2026-12-02", "Malaria", "Artemether", "", "", "0"]
            + ["4", "3", "1", "", "Severe malaria", "", "", "Admitted", "0"]
            + ["4", "4", "1", "0"]
            + ["0"]
        )
        output, database = run_script(answers)
        self.assertIn("Medical record updated.", output)
        self.assertIn("Severe malaria", output)
        self.assertIn("Admitted", output)
        database.close()

    def test_blank_required_value_is_asked_again(self):
        answers = ["1", "1", "", "Tendai", "0", "0"]
        output, database = run_script(answers)
        self.assertIn("First name is required.", output)
        database.close()

    def test_confirm_repeats_until_yes_or_no(self):
        console_output = []
        console = Console(ScriptedInput(["maybe", "yes"]), console_output.append)
        self.assertTrue(console.confirm("Sure?"))
        self.assertIn("Please answer y or n.", "\n".join(console_output))


if __name__ == "__main__":
    unittest.main()
