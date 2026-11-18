"""Abstract base service shared by every entity service."""

import sqlite3
from abc import ABC, abstractmethod

from utils.exceptions import BusinessRuleError, NotFoundError, ValidationError


class BaseService(ABC):
    """ABSTRACTION: defines what every service must provide (create, update, search).

    INHERITANCE: get_by_id, list_all, count and delete are written once here and
    reused by every child service.
    ENCAPSULATION: the Database object is stored in a protected attribute.
    """

    def __init__(self, database):
        self._db = database

    # ---- abstract members each child service must implement ----------------
    @property
    @abstractmethod
    def table_name(self):
        """Name of the SQLite table managed by the service."""

    @property
    @abstractmethod
    def entity_label(self):
        """Singular word used in messages, such as 'patient'."""

    @property
    @abstractmethod
    def columns(self):
        """Column names written by insert and update (everything except id)."""

    @abstractmethod
    def _from_row(self, row):
        """Convert a database row into an entity object."""

    @abstractmethod
    def create(self, entity):
        """Save a new entity."""

    @abstractmethod
    def update(self, entity):
        """Save changes to an existing entity."""

    @abstractmethod
    def search(self, keyword):
        """Return entities that match a keyword."""

    # ---- behaviour inherited by all services -------------------------------
    def get_by_id(self, entity_id):
        row = self._db.fetch_one(f"SELECT * FROM {self.table_name} WHERE id = ?", (entity_id,))
        if row is None:
            raise NotFoundError(f"No {self.entity_label} found with ID {entity_id}.")
        return self._from_row(row)

    def list_all(self):
        rows = self._db.fetch_all(f"SELECT * FROM {self.table_name} ORDER BY id")
        return [self._from_row(row) for row in rows]

    def count(self):
        return self._db.scalar(f"SELECT COUNT(*) FROM {self.table_name}")

    def delete(self, entity_id):
        self.get_by_id(entity_id)
        try:
            self._db.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (entity_id,))
        except sqlite3.IntegrityError:
            raise BusinessRuleError(
                f"The {self.entity_label} with ID {entity_id} cannot be deleted because "
                f"other records still depend on it."
            )

    # ---- protected helpers for child services ------------------------------
    def _insert(self, entity):
        data = entity.to_dict()
        names = ", ".join(self.columns)
        marks = ", ".join("?" for _ in self.columns)
        sql = f"INSERT INTO {self.table_name} ({names}) VALUES ({marks})"
        try:
            cursor = self._db.execute(sql, tuple(data[name] for name in self.columns))
        except sqlite3.IntegrityError as error:
            raise BusinessRuleError(f"The database rejected this {self.entity_label}: {error}")
        entity.id = cursor.lastrowid

    def _update_row(self, entity):
        if entity.id is None:
            raise BusinessRuleError(f"This {self.entity_label} has not been saved yet.")
        data = entity.to_dict()
        assignments = ", ".join(f"{name} = ?" for name in self.columns)
        sql = f"UPDATE {self.table_name} SET {assignments} WHERE id = ?"
        params = tuple(data[name] for name in self.columns) + (entity.id,)
        try:
            cursor = self._db.execute(sql, params)
        except sqlite3.IntegrityError as error:
            raise BusinessRuleError(f"The database rejected this {self.entity_label}: {error}")
        if cursor.rowcount == 0:
            raise NotFoundError(f"No {self.entity_label} found with ID {entity.id}.")

    def _require_exists(self, table, entity_id, label):
        row = self._db.fetch_one(f"SELECT 1 FROM {table} WHERE id = ?", (entity_id,))
        if row is None:
            raise NotFoundError(f"No {label} found with ID {entity_id}.")

    @staticmethod
    def _pattern(keyword):
        cleaned = "" if keyword is None else str(keyword).strip()
        if not cleaned:
            raise ValidationError("Search keyword is required.")
        return f"%{cleaned}%"
