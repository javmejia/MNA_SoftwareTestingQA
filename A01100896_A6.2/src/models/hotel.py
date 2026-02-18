"""Hotel domain model."""

from __future__ import annotations

from dataclasses import dataclass

from ..exceptions import ValidationError


@dataclass
class Hotel:
    """Represents a hotel."""

    hotel_id: str
    name: str
    location: str
    total_rooms: int
    available_rooms: int
    rating: float | None = None
    active: bool = True

    def __post_init__(self) -> None:
        if not self.hotel_id.strip():
            raise ValidationError("hotel_id cannot be empty")
        if not self.name.strip():
            raise ValidationError("name cannot be empty")
        if not self.location.strip():
            raise ValidationError("location cannot be empty")
        if self.total_rooms < 0:
            raise ValidationError("total_rooms must be >= 0")
        if self.available_rooms < 0:
            raise ValidationError("available_rooms must be >= 0")
        if self.available_rooms > self.total_rooms:
            raise ValidationError("available_rooms cannot exceed total_rooms")

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
            "available_rooms": self.available_rooms,
            "rating": self.rating,
            "active": self.active,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Hotel":
        """Create Hotel from dictionary."""
        try:
            return cls(
                hotel_id=str(data["hotel_id"]),
                name=str(data["name"]),
                location=str(data["location"]),
                total_rooms=int(data["total_rooms"]),
                available_rooms=int(data["available_rooms"]),
                rating=(
                    None
                    if data.get("rating") is None
                    else float(data.get("rating"))
                ),
                active=bool(data.get("active", True)),
            )
        except KeyError as exc:
            raise ValidationError(f"missing field: {exc.args[0]}") from exc
        except (TypeError, ValueError) as exc:
            raise ValidationError(f"invalid hotel data: {exc}") from exc
