# OOP Principles: Exactly Where Each One Appears

All paths are relative to the repository root. Every item below can be opened and checked.

## 1. Encapsulation (private attributes + controlled access)

| File | Class | What is private | Controlled access |
| --- | --- | --- | --- |
| `models/base_entity.py` | `BaseEntity` | `self.__id` | `id` property getter and validating setter (positive integer or `None`) |
| `models/person.py` | `Person` | `__first_name`, `__last_name`, `__national_id`, `__date_of_birth`, `__gender`, `__phone`, `__email` | Property getters and setters that call `Validators.*`; read-only `full_name` and `age` properties |
| `models/patient.py` | `Patient` | `__address`, `__province`, `__blood_group`, `__allergies`, `__emergency_contact_name`, `__emergency_contact_phone` | Property getters and validating setters |
| `models/doctor.py` | `Doctor` | `__specialization`, `__license_number`, `__department` | Property getters and validating setters |
| `models/appointment.py` | `Appointment` | `__patient_id`, `__doctor_id`, `__appointment_date`, `__appointment_time`, `__reason`, `__status` | Validating setters; status changes through `cancel()` which enforces business rules |
| `models/medical_record.py` | `MedicalRecord` | `__patient_id`, `__doctor_id`, `__appointment_id`, `__visit_date`, `__diagnosis`, `__treatment`, `__prescription`, `__notes` | Validating setters |
| `database/connection.py` | `Database` | `__connection`, `__path` | Methods `execute`, `fetch_one`, `fetch_all`, `scalar`, `close`; read-only `path` property |
| `services/dashboard_service.py` | `DashboardService` | `__patients`, `__doctors`, `__appointments`, `__records` | `get_summary()` and `render()` |
| `ui/console.py` | `Console` | `__input`, `__output` | `say`, `read`, `ask`, `ask_id`, `ask_choice`, `confirm` |

Proof in tests: `tests/test_person_models.py` (`EncapsulationTests`) shows setters rejecting bad values.

## 2. Inheritance (meaningful parent and child classes)

| Parent | Children | Files | What the children inherit |
| --- | --- | --- | --- |
| `BaseEntity` | `Person`, `Appointment`, `MedicalRecord` | `models/base_entity.py`, `person.py`, `appointment.py`, `medical_record.py` | The private `id`, its property, `__str__`, `__repr__` |
| `Person` | `Patient`, `Doctor` | `models/person.py`, `patient.py`, `doctor.py` | Name, National ID, date of birth, gender, phone, email, `full_name`, `age`, `_identity_lines()` |
| `BaseService` | `PatientService`, `DoctorService`, `AppointmentService`, `MedicalRecordService` | `services/base_service.py` and the four service files | `get_by_id`, `list_all`, `count`, `delete`, `_insert`, `_update_row`, `_require_exists`, `_pattern` |
| `Menu` | `MainMenu`, `PatientMenu`, `DoctorMenu`, `AppointmentMenu`, `MedicalRecordMenu` | `ui/menus.py` | The whole `run()` loop (show options, read choice, call handler, catch errors) |
| `EHRError` | `ValidationError`, `NotFoundError`, `DuplicateError`, `BusinessRuleError` | `utils/exceptions.py` | One base class so menus can catch every deliberate error |

Multi-level inheritance: `BaseEntity` -> `Person` -> `Patient` and `Doctor` (three levels).
Children call `super().__init__(...)` to reuse the parent constructor.

## 3. Polymorphism (overridden methods)

| Method | Declared in | Overridden in | Different behaviour |
| --- | --- | --- | --- |
| `describe()` | `BaseEntity` (abstract) | `Patient`, `Doctor`, `Appointment`, `MedicalRecord` | Each prints its own multi-line description |
| `to_dict()` | `BaseEntity` (abstract); concrete in `Person` | `Patient`, `Doctor` (extend the parent dict), `Appointment`, `MedicalRecord` | Each returns its own table columns |
| `get_role()` | `Person` (abstract) | `Patient` returns "Patient"; `Doctor` returns "Doctor" | Same call, different result (see `PolymorphismTests`) |
| `create()` | `BaseService` (abstract) | all four services | Patient/doctor check unique IDs; appointment checks existence and double booking; record checks links and completes the appointment |
| `update()` | `BaseService` (abstract) | all four services | Same idea: each applies its own rules before saving |
| `search()` | `BaseService` (abstract) | all four services | Each searches different columns |
| `table_name`, `entity_label`, `columns`, `_from_row` | `BaseService` (abstract) | all four services | Each supplies its own table and row conversion |
| `title`, `options()` | `Menu` (abstract) | all five menus | Each menu offers different options, all started by `run()` |
| `__str__()` | `BaseEntity` | (inherited) | Calls the overridden `describe()` of the actual object |

Example: `for entity in (patient, doctor, appointment, record): print(entity)` prints four different
descriptions through the same call.

## 4. Abstraction (abstract base classes from `abc`)

| File | Abstract class | Abstract members | Enforced by |
| --- | --- | --- | --- |
| `models/base_entity.py` | `BaseEntity(ABC)` | `to_dict()`, `describe()` | `tests/test_person_models.py::AbstractionTests` (instantiating raises `TypeError`) |
| `models/person.py` | `Person(BaseEntity)` | `get_role()` (and inherits abstract `describe()`) | same test |
| `services/base_service.py` | `BaseService(ABC)` | `table_name`, `entity_label`, `columns`, `_from_row()`, `create()`, `update()`, `search()` | `tests/test_patient_service.py::test_service_extends_abstract_base` |
| `ui/menus.py` | `Menu(ABC)` | `title`, `options()` | Python raises `TypeError` if a menu forgets them |

Abstraction hides the details of *how* each concrete class works behind a small contract: the
rest of the program only needs to know that an entity can `describe()` itself, a service can
`create()`, `update()` and `search()`, and a menu can `run()`.
