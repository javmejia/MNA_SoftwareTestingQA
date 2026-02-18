"""Reservation domain model."""

from dataclasses import dataclass
from datetime import datetime

from ..exceptions import ValidationError


def _validate_date(date_text: str, field_name: str) -> None:
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError as exc:
        raise ValidationError(f"{field_name} must use YYYY-MM-DD") from exc


@dataclass
class Reservation:
    """Represents a reservation."""

    reservation_id: str
    customer_id: str
    hotel_id: str
    check_in: str
    check_out: str
    num_rooms: int
    status: str
    created_at: str

    def __post_init__(self) -> None:
        if not self.reservation_id.strip():
            raise ValidationError("reservation_id cannot be empty")
        if not self.customer_id.strip():
            raise ValidationError("customer_id cannot be empty")
        if not self.hotel_id.strip():
            raise ValidationError("hotel_id cannot be empty")
        if self.num_rooms <= 0:
            raise ValidationError("num_rooms must be > 0")
        if self.status not in {"active", "cancelled"}:
            raise ValidationError("status must be active or cancelled")

        _validate_date(self.check_in, "check_in")
        _validate_date(self.check_out, "check_out")

        check_in_date = datetime.strptime(self.check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(self.check_out, "%Y-%m-%d").date()
        if check_out_date <= check_in_date:
            raise ValidationError("check_out must be later than check_in")

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
            "check_in": self.check_in,
            "check_out": self.check_out,
            "num_rooms": self.num_rooms,
            "status": self.status,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Reservation":
        """Create Reservation from dictionary."""
        try:
            return cls(
                reservation_id=str(data["reservation_id"]),
                customer_id=str(data["customer_id"]),
                hotel_id=str(data["hotel_id"]),
                check_in=str(data["check_in"]),
                check_out=str(data["check_out"]),
                num_rooms=int(data["num_rooms"]),
                status=str(data["status"]),
                created_at=str(data["created_at"]),
            )
        except KeyError as exc:
            raise ValidationError(f"missing field: {exc.args[0]}") from exc
        except (TypeError, ValueError) as exc:
            raise ValidationError(f"invalid reservation data: {exc}") from exc
