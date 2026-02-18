"""Business service exposing required system behaviors."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from uuid import uuid4

from ..exceptions import EntityNotFoundError, ValidationError
from ..models import Customer, Hotel, Reservation
from ..repositories import (
    CustomerRepository,
    HotelRepository,
    ReservationRepository,
)


# Required API signatures in this assignment include multiple parameters.
# pylint: disable=too-many-arguments,too-many-positional-arguments
class HotelReservationSystem:
    """Facade service implementing required operations."""

    def __init__(self, data_dir: str | Path = "data") -> None:
        """Initialize repositories using the provided data directory."""
        data_path = Path(data_dir)
        self.hotel_repository = HotelRepository(data_path / "hotels.json")
        self.customer_repository = CustomerRepository(
            data_path / "customers.json"
        )
        self.reservation_repository = ReservationRepository(
            data_path / "reservations.json"
        )

    # Hotels
    def create_hotel(
        self,
        hotel_id: str,
        name: str,
        location: str,
        total_rooms: int,
        available_rooms: int | None = None,
        rating: float | None = None,
        active: bool = True,
    ) -> None:
        """Create a new hotel record."""
        if available_rooms is None:
            available_rooms = total_rooms
        hotel = Hotel(
            hotel_id=hotel_id,
            name=name,
            location=location,
            total_rooms=total_rooms,
            available_rooms=available_rooms,
            rating=rating,
            active=active,
        )
        self.hotel_repository.create_hotel(hotel)

    def delete_hotel(self, hotel_id: str) -> bool:
        """Delete a hotel when there are no active reservations."""
        active_reservations = (
            self.reservation_repository.get_all_reservations()
        )
        if any(
            reservation.hotel_id == hotel_id
            and reservation.status == "active"
            for reservation in active_reservations
        ):
            raise ValidationError(
                "cannot delete hotel with active reservations"
            )
        return self.hotel_repository.delete_hotel(hotel_id)

    def display_hotel_info(self, hotel_id: str) -> dict | None:
        """Return hotel information by ID."""
        hotel = self.hotel_repository.get_hotel(hotel_id)
        return None if hotel is None else hotel.to_dict()

    def modify_hotel_info(self, hotel_id: str, **changes: object) -> bool:
        """Update hotel information by ID."""
        current = self.hotel_repository.get_hotel(hotel_id)
        if current is None:
            return False
        updated = Hotel(
            hotel_id=current.hotel_id,
            name=str(changes.get("name", current.name)),
            location=str(changes.get("location", current.location)),
            total_rooms=int(changes.get("total_rooms", current.total_rooms)),
            available_rooms=int(
                changes.get("available_rooms", current.available_rooms)
            ),
            rating=(
                None
                if changes.get("rating", current.rating) is None
                else float(changes.get("rating", current.rating))
            ),
            active=bool(changes.get("active", current.active)),
        )
        return self.hotel_repository.update_hotel(updated)

    def reserve_room(
        self,
        customer_id: str,
        hotel_id: str,
        check_in: str,
        check_out: str,
        num_rooms: int = 1,
    ) -> dict:
        """Reserve one or more rooms for a customer in a hotel."""
        reservation = self._build_reservation(
            customer_id=customer_id,
            hotel_id=hotel_id,
            check_in=check_in,
            check_out=check_out,
            num_rooms=num_rooms,
        )
        self.reservation_repository.create_reservation(reservation)
        self._update_hotel_capacity(hotel_id=hotel_id, room_delta=-num_rooms)
        return reservation.to_dict()

    def cancel_reservation(self, reservation_id: str) -> bool:
        """Cancel an existing reservation and release hotel capacity."""
        reservation = self.reservation_repository.get_reservation(
            reservation_id
        )
        if reservation is None:
            return False
        if reservation.status == "cancelled":
            return True

        cancelled = reservation.as_cancelled()
        was_updated = self.reservation_repository.update_reservation(cancelled)
        if was_updated:
            self._update_hotel_capacity(
                hotel_id=reservation.hotel_id, room_delta=reservation.num_rooms
            )
        return was_updated

    # Customers
    def create_customer(
        self,
        customer_id: str,
        full_name: str,
        email: str,
        phone: str,
        active: bool = True,
    ) -> None:
        """Create a new customer record."""
        customer = Customer(
            customer_id=customer_id,
            full_name=full_name,
            email=email,
            phone=phone,
            active=active,
        )
        self.customer_repository.create_customer(customer)

    def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer when there are no active reservations."""
        active_reservations = (
            self.reservation_repository.get_all_reservations()
        )
        if any(
            reservation.customer_id == customer_id
            and reservation.status == "active"
            for reservation in active_reservations
        ):
            raise ValidationError(
                "cannot delete customer with active reservations"
            )
        return self.customer_repository.delete_customer(customer_id)

    def display_customer_info(self, customer_id: str) -> dict | None:
        """Return customer information by ID."""
        customer = self.customer_repository.get_customer(customer_id)
        return None if customer is None else customer.to_dict()

    def modify_customer_info(
        self, customer_id: str, **changes: object
    ) -> bool:
        """Update customer information by ID."""
        current = self.customer_repository.get_customer(customer_id)
        if current is None:
            return False
        updated = Customer(
            customer_id=current.customer_id,
            full_name=str(changes.get("full_name", current.full_name)),
            email=str(changes.get("email", current.email)),
            phone=str(changes.get("phone", current.phone)),
            active=bool(changes.get("active", current.active)),
        )
        return self.customer_repository.update_customer(updated)

    # Reservations
    def create_reservation(
        self,
        customer_id: str,
        hotel_id: str,
        check_in: str,
        check_out: str,
        num_rooms: int = 1,
    ) -> dict:
        """Create a reservation between a customer and a hotel."""
        return self.reserve_room(
            customer_id=customer_id,
            hotel_id=hotel_id,
            check_in=check_in,
            check_out=check_out,
            num_rooms=num_rooms,
        )

    def display_reservation_info(self, reservation_id: str) -> dict | None:
        """Return reservation information by ID."""
        reservation = self.reservation_repository.get_reservation(
            reservation_id
        )
        return None if reservation is None else reservation.to_dict()

    def _build_reservation(
        self,
        customer_id: str,
        hotel_id: str,
        check_in: str,
        check_out: str,
        num_rooms: int,
    ) -> Reservation:
        """Build a validated reservation instance."""
        customer = self.customer_repository.get_customer(customer_id)
        if customer is None:
            raise EntityNotFoundError(f"customer not found: {customer_id}")
        if not customer.active:
            raise ValidationError(f"customer is inactive: {customer_id}")

        hotel = self.hotel_repository.get_hotel(hotel_id)
        if hotel is None:
            raise EntityNotFoundError(f"hotel not found: {hotel_id}")
        if not hotel.active:
            raise ValidationError(f"hotel is inactive: {hotel_id}")
        if hotel.available_rooms < num_rooms:
            raise ValidationError("insufficient room availability")

        return Reservation(
            reservation_id=self._next_reservation_id(),
            customer_id=customer_id,
            hotel_id=hotel_id,
            check_in=check_in,
            check_out=check_out,
            num_rooms=num_rooms,
            status="active",
            created_at=datetime.utcnow().isoformat(timespec="seconds"),
        )

    def _update_hotel_capacity(self, hotel_id: str, room_delta: int) -> None:
        """Adjust hotel available room count by delta."""
        hotel = self.hotel_repository.get_hotel(hotel_id)
        if hotel is None:
            raise EntityNotFoundError(f"hotel not found: {hotel_id}")

        new_available = hotel.available_rooms + room_delta
        if new_available < 0 or new_available > hotel.total_rooms:
            raise ValidationError("invalid room capacity update")

        updated_hotel = Hotel(
            hotel_id=hotel.hotel_id,
            name=hotel.name,
            location=hotel.location,
            total_rooms=hotel.total_rooms,
            available_rooms=new_available,
            rating=hotel.rating,
            active=hotel.active,
        )
        self.hotel_repository.update_hotel(updated_hotel)

    @staticmethod
    def _next_reservation_id() -> str:
        """Return a new reservation identifier."""
        return f"R-{uuid4().hex[:12].upper()}"
