# EHR-System: Electronic Health Record Management System

## Overview

EHR-System is a menu-driven Electronic Health Record (EHR) application developed in Python with SQLite for persistent data storage. The system enables healthcare providers to manage patients, doctors, appointments, and medical records within a single integrated platform.

The project was developed as part of the MSc Medical Analytics and Informatics programme at the University of Zimbabwe and demonstrates the application of object-oriented programming principles including abstraction, encapsulation, inheritance, and polymorphism.

---

## Key Features

### Patient Management

- Register new patients
- Search patient records
- Update patient information
- Delete patient records
- View individual patient details
- View all registered patients

### Doctor Management

- Register doctors
- Search doctor records
- Update doctor information
- Delete doctor records
- View individual doctor details
- View all registered doctors

### Appointment Management

- Schedule appointments
- Update appointments
- Cancel appointments while preserving history
- Filter appointments by patient, doctor, or status
- Prevent double booking of doctors

### Medical Records

- Create patient medical records
- Update medical records
- View patient history
- View individual consultation records
- Automatically update appointment status after consultation

### Dashboard

- Patient statistics
- Doctor statistics
- Appointment statistics
- Medical record statistics
- Appointment status summaries

### Validation and Error Handling

- National ID validation
- Phone number validation
- Email validation
- Date and time validation
- Blood group validation
- Province validation
- Medical licence validation
- User-friendly error handling

---

## Technologies Used

- Python 3
- SQLite
- Object-Oriented Programming (OOP)
- unittest
- Git
- GitHub

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YeuMawuka/OOP_Mini_Project.git
cd OOP_Mini_Project
```

No third-party packages are required.

## Running the Application

```bash
python main.py
```

Alternative commands:

```bash
python3 main.py
```

or

```bash
py main.py
```

## Running Tests

```bash
python -m unittest discover -s tests -t . -v
```

---

## Project Structure

```text
EHR-System/
├── main.py
├── models/
├── services/
├── database/
├── ui/
├── utils/
├── tests/
└── docs/
```

---

## Contributors

- Nicodimus
- Yeukai

This project was developed collaboratively using GitHub for version control, testing, documentation, integration, and project management.

---

## Academic Purpose

This project was developed for academic and educational purposes as part of the MSc Medical Analytics and Informatics programme at the University of Zimbabwe.
