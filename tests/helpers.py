"""Shared helpers that build valid sample objects for the tests."""

# Imports are done inside each function so that this file works at every step of
# the Git history, even before the classes it builds have been merged.


def make_database():
    """Return a fresh in-memory database."""
    from database.connection import Database
    return Database(":memory:")


def make_patient(**overrides):
    from models.patient import Patient
    values = {
        "first_name": "Tendai",
        "last_name": "Moyo",
        "national_id": "63-123456-A-42",
        "date_of_birth": "1990-05-17",
        "gender": "Female",
        "phone": "0771234567",
        "email": "tendai.moyo@example.co.zw",
        "address": "12 Samora Machel Avenue",
        "province": "Harare",
        "blood_group": "O+",
        "allergies": "Penicillin",
        "emergency_contact_name": "Rudo Moyo",
        "emergency_contact_phone": "0712345678",
    }
    values.update(overrides)
    return Patient(**values)


def make_doctor(**overrides):
    from models.doctor import Doctor
    values = {
        "first_name": "Farai",
        "last_name": "Chikwanha",
        "national_id": "08-765432-B-12",
        "date_of_birth": "1980-03-02",
        "gender": "Male",
        "phone": "+263772000111",
        "email": "f.chikwanha@example.co.zw",
        "specialization": "Cardiology",
        "license_number": "MDPCZ-10234",
        "department": "Cardiology",
    }
    values.update(overrides)
    return Doctor(**values)


def make_appointment(patient_id=1, doctor_id=1, **overrides):
    from models.appointment import Appointment
    values = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "appointment_date": "2026-12-01",
        "appointment_time": "09:30",
        "reason": "Chest pain review",
    }
    values.update(overrides)
    return Appointment(**values)


def make_record(patient_id=1, doctor_id=1, **overrides):
    from models.medical_record import MedicalRecord
    values = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "visit_date": "2026-12-01",
        "diagnosis": "Hypertension",
        "treatment": "Lifestyle changes and monitoring",
        "prescription": "Amlodipine 5mg daily",
        "notes": "Review in four weeks",
    }
    values.update(overrides)
    return MedicalRecord(**values)
