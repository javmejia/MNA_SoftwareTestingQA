"""Customer domain model."""

from __future__ import annotations

from dataclasses import dataclass

from ..exceptions import ValidationError


@dataclass
class Customer:
    """Represents a customer."""

    customer_id: str
    full_name: str
    email: str
    phone: str
    active: bool = True

    def __post_init__(self) -> None:
        if not self.customer_id.strip():
            raise ValidationError("customer_id cannot be empty")
        if not self.full_name.strip():
            raise ValidationError("full_name cannot be empty")
        if not self.email.strip():
            raise ValidationError("email cannot be empty")
        if "@" not in self.email:
            raise ValidationError("email format is invalid")
        if not self.phone.strip():
            raise ValidationError("phone cannot be empty")

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "customer_id": self.customer_id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "active": self.active,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Customer":
        """Create Customer from dictionary."""
        try:
            return cls(
                customer_id=str(data["customer_id"]),
                full_name=str(data["full_name"]),
                email=str(data["email"]),
                phone=str(data["phone"]),
                active=bool(data.get("active", True)),
            )
        except KeyError as exc:
            raise ValidationError(f"missing field: {exc.args[0]}") from exc
        except (TypeError, ValueError) as exc:
            raise ValidationError(f"invalid customer data: {exc}") from exc
