"""Unit tests for domain models."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.exceptions import ValidationError
from src.models import Customer, Hotel, Reservation


class TestHotelModel(unittest.TestCase):
    """Tests for the Hotel model."""

    def test_hotel_to_from_dict(self) -> None:
        hotel = Hotel(
            hotel_id="H001",
            name="City Inn",
            location="MTY",
            total_rooms=10,
            available_rooms=9,
            rating=4.2,
            active=True,
        )
        data = hotel.to_dict()
        rebuilt = Hotel.from_dict(data)
        self.assertEqual(rebuilt.hotel_id, "H001")
        self.assertEqual(rebuilt.available_rooms, 9)

    def test_hotel_invalid_values_raise(self) -> None:
        with self.assertRaises(ValidationError):
            Hotel("", "A", "B", 1, 1)
        with self.assertRaises(ValidationError):
            Hotel("H1", "A", "B", -1, 0)
        with self.assertRaises(ValidationError):
            Hotel("H1", "A", "B", 1, 2)

    def test_hotel_from_dict_missing_field(self) -> None:
        with self.assertRaises(ValidationError):
            Hotel.from_dict({"hotel_id": "H1"})


class TestCustomerModel(unittest.TestCase):
    """Tests for the Customer model."""

    def test_customer_to_from_dict(self) -> None:
        customer = Customer(
            customer_id="C001",
            full_name="Jane Doe",
            email="jane@example.com",
            phone="555-1000",
        )
        data = customer.to_dict()
        rebuilt = Customer.from_dict(data)
        self.assertEqual(rebuilt.customer_id, "C001")
        self.assertEqual(rebuilt.email, "jane@example.com")

    def test_customer_invalid_values_raise(self) -> None:
        with self.assertRaises(ValidationError):
            Customer("", "Jane", "jane@example.com", "555")
        with self.assertRaises(ValidationError):
            Customer("C1", "Jane", "invalid-email", "555")

    def test_customer_from_dict_missing_field(self) -> None:
        with self.assertRaises(ValidationError):
            Customer.from_dict({"customer_id": "C1"})


class TestReservationModel(unittest.TestCase):
    """Tests for the Reservation model."""

    def _valid_reservation(self) -> Reservation:
        return Reservation(
            reservation_id="R001",
            customer_id="C001",
            hotel_id="H001",
            check_in="2026-03-01",
            check_out="2026-03-03",
            num_rooms=1,
            status="active",
            created_at="2026-02-18T12:00:00",
        )

    def test_reservation_to_from_dict(self) -> None:
        reservation = self._valid_reservation()
        rebuilt = Reservation.from_dict(reservation.to_dict())
        self.assertEqual(rebuilt.reservation_id, "R001")
        self.assertEqual(rebuilt.status, "active")

    def test_reservation_invalid_values_raise(self) -> None:
        with self.assertRaises(ValidationError):
            Reservation(
                reservation_id="",
                customer_id="C001",
                hotel_id="H001",
                check_in="2026-03-01",
                check_out="2026-03-03",
                num_rooms=1,
                status="active",
                created_at="2026-02-18T12:00:00",
            )
        with self.assertRaises(ValidationError):
            Reservation(
                reservation_id="R001",
                customer_id="C001",
                hotel_id="H001",
                check_in="2026-03-01",
                check_out="2026-03-01",
                num_rooms=1,
                status="active",
                created_at="2026-02-18T12:00:00",
            )
        with self.assertRaises(ValidationError):
            Reservation(
                reservation_id="R001",
                customer_id="C001",
                hotel_id="H001",
                check_in="03-01-2026",
                check_out="2026-03-03",
                num_rooms=1,
                status="active",
                created_at="2026-02-18T12:00:00",
            )

    def test_reservation_from_dict_missing_field(self) -> None:
        with self.assertRaises(ValidationError):
            Reservation.from_dict({"reservation_id": "R1"})

    def test_reservation_as_cancelled(self) -> None:
        cancelled = self._valid_reservation().as_cancelled()
        self.assertEqual(cancelled.status, "cancelled")


if __name__ == "__main__":
    unittest.main()
