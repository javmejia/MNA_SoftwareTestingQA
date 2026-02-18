"""Reservation repository."""

from __future__ import annotations

from pathlib import Path

from ..exceptions import DuplicateEntityError
from ..models import Reservation
from .base_json_repository import BaseJsonRepository


class ReservationRepository:
    """Manages Reservation persistence operations."""

    def __init__(self, file_path: str | Path) -> None:
        self._repo = BaseJsonRepository(
            file_path, Reservation.from_dict, "reservation"
        )

    def create_reservation(self, reservation: Reservation) -> None:
        reservations = self._repo.load_all()
        if any(
            existing.reservation_id == reservation.reservation_id
            for existing in reservations
        ):
            raise DuplicateEntityError(
                f"reservation already exists: {reservation.reservation_id}"
            )
        reservations.append(reservation)
        self._repo.save_all(reservations, lambda item: item.to_dict())

    def cancel_reservation(self, reservation_id: str) -> bool:
        reservations = self._repo.load_all()
        updated = False
        for idx, reservation in enumerate(reservations):
            if reservation.reservation_id == reservation_id:
                if reservation.status == "cancelled":
                    return True
                reservations[idx] = Reservation(
                    reservation_id=reservation.reservation_id,
                    customer_id=reservation.customer_id,
                    hotel_id=reservation.hotel_id,
                    check_in=reservation.check_in,
                    check_out=reservation.check_out,
                    num_rooms=reservation.num_rooms,
                    status="cancelled",
                    created_at=reservation.created_at,
                )
                updated = True
                break
        if updated:
            self._repo.save_all(reservations, lambda item: item.to_dict())
        return updated

    def get_reservation(self, reservation_id: str) -> Reservation | None:
        for reservation in self._repo.load_all():
            if reservation.reservation_id == reservation_id:
                return reservation
        return None

    def get_all_reservations(self) -> list[Reservation]:
        return self._repo.load_all()

    def update_reservation(self, reservation: Reservation) -> bool:
        reservations = self._repo.load_all()
        updated = False
        for idx, current in enumerate(reservations):
            if current.reservation_id == reservation.reservation_id:
                reservations[idx] = reservation
                updated = True
                break
        if updated:
            self._repo.save_all(reservations, lambda item: item.to_dict())
        return updated
