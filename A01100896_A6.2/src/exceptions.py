"""Custom exceptions for the hotel reservation system."""


class EntityNotFoundError(Exception):
    """Raised when an entity is not found."""


class ValidationError(Exception):
    """Raised when input or entity data is invalid."""


class DuplicateEntityError(Exception):
    """Raised when attempting to create an already existing entity."""


class PersistenceError(Exception):
    """Raised for persistent storage operation failures."""

