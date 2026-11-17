"""SQLite schema for the EHR Management System."""

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL CHECK (length(trim(first_name)) > 0),
    last_name TEXT NOT NULL CHECK (length(trim(last_name)) > 0),
    national_id TEXT NOT NULL UNIQUE,
    date_of_birth TEXT NOT NULL,
    gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female', 'Other')),
    phone TEXT NOT NULL,
    email TEXT NOT NULL DEFAULT '',
    address TEXT NOT NULL DEFAULT '',
    province TEXT NOT NULL CHECK (province IN (
        'Bulawayo', 'Harare', 'Manicaland', 'Mashonaland Central',
        'Mashonaland East', 'Mashonaland West', 'Masvingo',
        'Matabeleland North', 'Matabeleland South', 'Midlands')),
    blood_group TEXT NOT NULL DEFAULT 'Unknown' CHECK (blood_group IN (
        'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', 'Unknown')),
    allergies TEXT NOT NULL DEFAULT '',
    emergency_contact_name TEXT NOT NULL DEFAULT '',
    emergency_contact_phone TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL CHECK (length(trim(first_name)) > 0),
    last_name TEXT NOT NULL CHECK (length(trim(last_name)) > 0),
    national_id TEXT NOT NULL UNIQUE,
    date_of_birth TEXT NOT NULL,
    gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female', 'Other')),
    phone TEXT NOT NULL,
    email TEXT NOT NULL DEFAULT '',
    specialization TEXT NOT NULL,
    license_number TEXT NOT NULL UNIQUE,
    department TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""
