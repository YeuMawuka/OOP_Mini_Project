"""SQLite connection wrapper built on Python's sqlite3 module."""

import os
import sqlite3

from database.schema import SCHEMA_SQL

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATABASE_PATH = os.path.join(PROJECT_ROOT, "data", "ehr.db")


class Database:
    """ENCAPSULATION: the sqlite3 connection is private; callers use methods only.

    Opening a Database creates the file (and its folder) when needed and makes
    sure every table exists, so records survive closing and reopening the program.
    """

    def __init__(self, path=DEFAULT_DATABASE_PATH):
        self.__path = path
        if path != ":memory:":
            folder = os.path.dirname(os.path.abspath(path))
            os.makedirs(folder, exist_ok=True)
        self.__connection = sqlite3.connect(path)
        self.__connection.row_factory = sqlite3.Row
        self.__connection.execute("PRAGMA foreign_keys = ON")
        self.initialize_schema()

    @property
    def path(self):
        return self.__path

    def initialize_schema(self):
        """Create every table and index that does not exist yet."""
        self.__connection.executescript(SCHEMA_SQL)
        self.__connection.commit()

    def execute(self, sql, params=()):
        """Run one write statement and commit it; roll back if it fails."""
        try:
            cursor = self.__connection.execute(sql, params)
            self.__connection.commit()
            return cursor
        except sqlite3.Error:
            self.__connection.rollback()
            raise

    def fetch_one(self, sql, params=()):
        """Return the first matching row, or None."""
        return self.__connection.execute(sql, params).fetchone()

    def fetch_all(self, sql, params=()):
        """Return every matching row as a list."""
        return self.__connection.execute(sql, params).fetchall()

    def scalar(self, sql, params=()):
        """Return the first column of the first row (used for COUNT queries)."""
        return self.__connection.execute(sql, params).fetchone()[0]

    def close(self):
        """Close the connection."""
        self.__connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False
