"""MedicalRecord: the clinical note written after a patient visit."""

from models.base_entity import BaseEntity
from utils.validators import Validators


class MedicalRecord(BaseEntity):
    """INHERITANCE: MedicalRecord extends the abstract BaseEntity.

    ENCAPSULATION: every clinical field is private and validated on assignment.
    POLYMORPHISM: describe() and to_dict() override the abstract versions.
    """

    def __init__(self, patient_id, doctor_id, visit_date, diagnosis, treatment,
                 prescription="", notes="", appointment_id=None, entity_id=None):
        super().__init__(entity_id)
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_id = appointment_id
        self.visit_date = visit_date
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.prescription = prescription
        self.notes = notes

    @property
    def patient_id(self):
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value):
        self.__patient_id = Validators.positive_int(value, "Patient ID")

    @property
    def doctor_id(self):
        return self.__doctor_id

    @doctor_id.setter
    def doctor_id(self, value):
        self.__doctor_id = Validators.positive_int(value, "Doctor ID")

    @property
    def appointment_id(self):
        return self.__appointment_id

    @appointment_id.setter
    def appointment_id(self, value):
        if value is None or value == "":
            self.__appointment_id = None
        else:
            self.__appointment_id = Validators.positive_int(value, "Appointment ID")

    @property
    def visit_date(self):
        return self.__visit_date

    @visit_date.setter
    def visit_date(self, value):
        self.__visit_date = Validators.date_value(value, "Visit date")

    @property
    def diagnosis(self):
        return self.__diagnosis

    @diagnosis.setter
    def diagnosis(self, value):
        self.__diagnosis = Validators.text(value, "Diagnosis", 200)

    @property
    def treatment(self):
        return self.__treatment

    @treatment.setter
    def treatment(self, value):
        self.__treatment = Validators.text(value, "Treatment", 500)

    @property
    def prescription(self):
        return self.__prescription

    @prescription.setter
    def prescription(self, value):
        self.__prescription = Validators.text(value, "Prescription", 500, required=False)

    @property
    def notes(self):
        return self.__notes

    @notes.setter
    def notes(self, value):
        self.__notes = Validators.text(value, "Notes", 1000, required=False)

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "appointment_id": self.appointment_id,
            "visit_date": self.visit_date,
            "diagnosis": self.diagnosis,
            "treatment": self.treatment,
            "prescription": self.prescription,
            "notes": self.notes,
        }

    def describe(self):
        appointment = self.appointment_id if self.appointment_id is not None else "none"
        return (
            f"Medical record #{self.id}: visit on {self.visit_date}\n"
            f"  Patient ID   : {self.patient_id}\n"
            f"  Doctor ID    : {self.doctor_id}\n"
            f"  Appointment  : {appointment}\n"
            f"  Diagnosis    : {self.diagnosis}\n"
            f"  Treatment    : {self.treatment}\n"
            f"  Prescription : {self.prescription or 'none'}\n"
            f"  Notes        : {self.notes or 'none'}"
        )

    @classmethod
    def from_row(cls, row):
        """Build a MedicalRecord from a database row."""
        return cls(
            patient_id=row["patient_id"],
            doctor_id=row["doctor_id"],
            visit_date=row["visit_date"],
            diagnosis=row["diagnosis"],
            treatment=row["treatment"],
            prescription=row["prescription"],
            notes=row["notes"],
            appointment_id=row["appointment_id"],
            entity_id=row["id"],
        )
