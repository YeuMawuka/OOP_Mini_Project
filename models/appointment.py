"""Appointment: a booked visit between a patient and a doctor."""

from models.base_entity import BaseEntity
from utils.exceptions import BusinessRuleError
from utils.validators import Validators


class Appointment(BaseEntity):
    """INHERITANCE: Appointment extends the abstract BaseEntity.

    ENCAPSULATION: the status can only change through validated methods.
    POLYMORPHISM: describe() and to_dict() override the abstract versions.
    """

    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

    def __init__(self, patient_id, doctor_id, appointment_date, appointment_time,
                 reason, status="Scheduled", entity_id=None):
        super().__init__(entity_id)
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.reason = reason
        self.status = status

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
    def appointment_date(self):
        return self.__appointment_date

    @appointment_date.setter
    def appointment_date(self, value):
        self.__appointment_date = Validators.date_value(value, "Appointment date")

    @property
    def appointment_time(self):
        return self.__appointment_time

    @appointment_time.setter
    def appointment_time(self, value):
        self.__appointment_time = Validators.time_value(value, "Appointment time")

    @property
    def reason(self):
        return self.__reason

    @reason.setter
    def reason(self, value):
        self.__reason = Validators.text(value, "Reason", 200)

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = Validators.choice(value, Validators.APPOINTMENT_STATUSES, "Status")

    def cancel(self):
        """Cancel the appointment, enforcing the hospital's business rules."""
        if self.__status == self.CANCELLED:
            raise BusinessRuleError("This appointment is already cancelled.")
        if self.__status == self.COMPLETED:
            raise BusinessRuleError("A completed appointment cannot be cancelled.")
        self.__status = self.CANCELLED

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "appointment_date": self.appointment_date,
            "appointment_time": self.appointment_time,
            "reason": self.reason,
            "status": self.status,
        }

    def describe(self):
        return (
            f"Appointment #{self.id}: {self.appointment_date} at {self.appointment_time}\n"
            f"  Patient ID : {self.patient_id}\n"
            f"  Doctor ID  : {self.doctor_id}\n"
            f"  Reason     : {self.reason}\n"
            f"  Status     : {self.status}"
        )

    @classmethod
    def from_row(cls, row):
        """Build an Appointment from a database row."""
        return cls(
            patient_id=row["patient_id"],
            doctor_id=row["doctor_id"],
            appointment_date=row["appointment_date"],
            appointment_time=row["appointment_time"],
            reason=row["reason"],
            status=row["status"],
            entity_id=row["id"],
        )
