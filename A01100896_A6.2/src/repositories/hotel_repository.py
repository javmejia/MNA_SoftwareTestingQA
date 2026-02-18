"""Hotel repository."""

from __future__ import annotations

from pathlib import Path

from ..exceptions import DuplicateEntityError
from ..models import Hotel
from .base_json_repository import BaseJsonRepository


class HotelRepository:
    """Manages Hotel persistence operations."""

    def __init__(self, file_path: str | Path) -> None:
        """Initialize repository with the hotel storage file path."""
        self._repo = BaseJsonRepository(file_path, Hotel.from_dict, "hotel")

    def create_hotel(self, hotel: Hotel) -> None:
        """Create a hotel if it does not already exist."""
        hotels = self._repo.load_all()
        if any(existing.hotel_id == hotel.hotel_id for existing in hotels):
            raise DuplicateEntityError(
                f"hotel already exists: {hotel.hotel_id}"
            )
        hotels.append(hotel)
        self._repo.save_all(hotels, lambda item: item.to_dict())

    def delete_hotel(self, hotel_id: str) -> bool:
        """Delete a hotel by ID."""
        hotels = self._repo.load_all()
        filtered = [hotel for hotel in hotels if hotel.hotel_id != hotel_id]
        deleted = len(filtered) != len(hotels)
        if deleted:
            self._repo.save_all(filtered, lambda item: item.to_dict())
        return deleted

    def get_hotel(self, hotel_id: str) -> Hotel | None:
        """Return a hotel by ID or None when not found."""
        for hotel in self._repo.load_all():
            if hotel.hotel_id == hotel_id:
                return hotel
        return None

    def get_all_hotels(self) -> list[Hotel]:
        """Return all valid hotels from storage."""
        return self._repo.load_all()

    def update_hotel(self, hotel: Hotel) -> bool:
        """Update an existing hotel by ID."""
        hotels = self._repo.load_all()
        updated = False
        for idx, current in enumerate(hotels):
            if current.hotel_id == hotel.hotel_id:
                hotels[idx] = hotel
                updated = True
                break
        if updated:
            self._repo.save_all(hotels, lambda item: item.to_dict())
        return updated
