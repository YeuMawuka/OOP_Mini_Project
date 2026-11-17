"""Abstract base class shared by every entity stored in the database."""

from abc import ABC, abstractmethod

from utils.exceptions import ValidationError


class BaseEntity(ABC):
    """ABSTRACTION: the contract every EHR entity must follow.

    ENCAPSULATION: the identifier is stored in a private attribute and is only
    reachable through the controlled `id` property.
    """

    def __init__(self, entity_id=None):
        self.__id = None
        self.id = entity_id

    @property
    def id(self):
        """Database identifier (None until the entity has been saved)."""
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValidationError("Identifier must be a positive whole number or None.")
        self.__id = value

    @abstractmethod
    def to_dict(self):
        """Return the entity as a dictionary whose keys match the table columns."""

    @abstractmethod
    def describe(self):
        """Return a human-readable description (overridden by every child class)."""

    def __str__(self):
        return self.describe()

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r})"
