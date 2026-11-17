"""Dashboard service: summary statistics for the whole system."""

from utils.formatters import TableFormatter


class DashboardService:
    """Combines the other services (composition) to report system totals."""

    def __init__(self, patient_service, doctor_service, appointment_service,
                 medical_record_service):
        self.__patients = patient_service
        self.__doctors = doctor_service
        self.__appointments = appointment_service
        self.__records = medical_record_service

    def get_summary(self):
        """Return the dashboard figures as a dictionary."""
        return {
            "total_patients": self.__patients.count(),
            "total_doctors": self.__doctors.count(),
            "total_appointments": self.__appointments.count(),
            "total_medical_records": self.__records.count(),
            "appointments_by_status": self.__appointments.count_by_status(),
        }

    def render(self):
        """Return the dashboard as printable text."""
        summary = self.get_summary()
        lines = [
            TableFormatter.heading("EHR Dashboard"),
            f"Total patients        : {summary['total_patients']}",
            f"Total doctors         : {summary['total_doctors']}",
            f"Total appointments    : {summary['total_appointments']}",
            f"Total medical records : {summary['total_medical_records']}",
            "",
            "Appointments by status:",
        ]
        for status, total in summary["appointments_by_status"].items():
            lines.append(f"  {status:<10}: {total}")
        return "\n".join(lines)
