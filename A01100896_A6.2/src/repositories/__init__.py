"""Repository classes."""

from .customer_repository import CustomerRepository
from .hotel_repository import HotelRepository
from .reservation_repository import ReservationRepository

__all__ = ["HotelRepository", "CustomerRepository", "ReservationRepository"]

