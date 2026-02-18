"""Unit tests for service layer behaviors."""
# pylint: disable=import-error,wrong-import-position,missing-function-docstring

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.exceptions import EntityNotFoundError, ValidationError  # noqa: E402
from src.services.hotel_reservation_system import HotelReservationSystem  # noqa: E402


class TestHotelReservationSystem(unittest.TestCase):
    """Tests for required hotel/customer/reservation operations."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.service = HotelReservationSystem(self.temp_dir)
        self.service.create_hotel("H001", "City Inn", "MTY", 10)
        self.service.create_customer(
            "C001",
            "Jane Doe",
            "jane@example.com",
            "555-0001",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_display_operations_return_none_for_missing_entities(self) -> None:
        self.assertIsNone(self.service.display_hotel_info("H404"))
        self.assertIsNone(self.service.display_customer_info("C404"))
        self.assertIsNone(self.service.display_reservation_info("R404"))

    def test_modify_operations_update_existing_entities(self) -> None:
        self.assertTrue(
            self.service.modify_hotel_info("H001", name="Beach Inn")
        )
        self.assertEqual(
            self.service.display_hotel_info("H001")["name"],
            "Beach Inn",
        )

        self.assertTrue(
            self.service.modify_customer_info(
                "C001", phone="777-1234", full_name="Jane Updated"
            )
        )
        customer = self.service.display_customer_info("C001")
        self.assertEqual(customer["phone"], "777-1234")
        self.assertEqual(customer["full_name"], "Jane Updated")

    def test_modify_operations_return_false_for_missing_entities(self) -> None:
        self.assertFalse(
            self.service.modify_hotel_info("H404", name="Missing")
        )
        self.assertFalse(
            self.service.modify_customer_info("C404", full_name="Missing")
        )

    def test_reservation_lifecycle_and_capacity_changes(self) -> None:
        reservation = self.service.create_reservation(
            "C001",
            "H001",
            "2026-03-01",
            "2026-03-03",
            2,
        )
        self.assertEqual(reservation["status"], "active")
        self.assertTrue(reservation["reservation_id"].startswith("R-"))
        self.assertEqual(
            self.service.display_hotel_info("H001")["available_rooms"],
            8,
        )

        reservation_id = reservation["reservation_id"]
        self.assertTrue(self.service.cancel_reservation(reservation_id))
        self.assertTrue(self.service.cancel_reservation(reservation_id))
        self.assertFalse(self.service.cancel_reservation("R404"))
        self.assertEqual(
            self.service.display_hotel_info("H001")["available_rooms"],
            10,
        )

    def test_delete_blocked_by_active_reservation(self) -> None:
        reservation = self.service.create_reservation(
            "C001",
            "H001",
            "2026-03-01",
            "2026-03-03",
            1,
        )
        with self.assertRaises(ValidationError):
            self.service.delete_hotel("H001")
        with self.assertRaises(ValidationError):
            self.service.delete_customer("C001")

        self.assertTrue(
            self.service.cancel_reservation(reservation["reservation_id"])
        )
        self.assertTrue(self.service.delete_hotel("H001"))
        self.assertTrue(self.service.delete_customer("C001"))

    def test_create_hotel_defaults_available_rooms_to_total(self) -> None:
        self.service.create_hotel("H002", "Airport Inn", "MTY", 4)
        hotel = self.service.display_hotel_info("H002")
        self.assertEqual(hotel["available_rooms"], 4)

    def test_reservation_requires_existing_customer_and_hotel(self) -> None:
        with self.assertRaises(EntityNotFoundError):
            self.service.create_reservation(
                "C404", "H001", "2026-03-01", "2026-03-03", 1
            )
        with self.assertRaises(EntityNotFoundError):
            self.service.create_reservation(
                "C001", "H404", "2026-03-01", "2026-03-03", 1
            )

    def test_reservation_rejects_inactive_or_unavailable(self) -> None:
        self.assertTrue(
            self.service.modify_customer_info("C001", active=False)
        )
        with self.assertRaises(ValidationError):
            self.service.create_reservation(
                "C001", "H001", "2026-03-01", "2026-03-03", 1
            )

        self.assertTrue(self.service.modify_customer_info("C001", active=True))
        self.assertTrue(self.service.modify_hotel_info("H001", active=False))
        with self.assertRaises(ValidationError):
            self.service.create_reservation(
                "C001", "H001", "2026-03-01", "2026-03-03", 1
            )

        self.assertTrue(self.service.modify_hotel_info("H001", active=True))
        with self.assertRaises(ValidationError):
            self.service.create_reservation(
                "C001", "H001", "2026-03-01", "2026-03-03", 100
            )


if __name__ == "__main__":
    unittest.main()
