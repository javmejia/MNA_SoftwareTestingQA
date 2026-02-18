"""Unit tests for repositories and persistence behavior."""
# pylint: disable=import-error,wrong-import-position
# pylint: disable=missing-function-docstring,duplicate-code

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.exceptions import DuplicateEntityError, PersistenceError  # noqa: E402
from src.models import Customer, Hotel, Reservation  # noqa: E402
from src.repositories.base_json_repository import BaseJsonRepository  # noqa: E402
from src.repositories.customer_repository import CustomerRepository  # noqa: E402
from src.repositories.hotel_repository import HotelRepository  # noqa: E402
from src.repositories.reservation_repository import ReservationRepository  # noqa: E402


class TestBaseJsonRepository(unittest.TestCase):
    """Tests for BaseJsonRepository behavior, including Req 5 cases."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.file_path = Path(self.temp_dir) / "hotels.json"
        self.repo = BaseJsonRepository(
            self.file_path, Hotel.from_dict, "hotel"
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_load_all_skips_invalid_records_and_continues(self) -> None:
        valid = {
            "hotel_id": "H001",
            "name": "City Inn",
            "location": "MTY",
            "total_rooms": 10,
            "available_rooms": 8,
            "rating": 4.0,
            "active": True,
        }
        invalid_model = {
            "hotel_id": "",
            "name": "Bad",
            "location": "MTY",
            "total_rooms": 10,
            "available_rooms": 8,
        }
        self.file_path.write_text(
            json.dumps([valid, invalid_model, "not-a-dict"]),
            encoding="utf-8",
        )

        with patch("builtins.print") as mock_print:
            hotels = self.repo.load_all()

        self.assertEqual(len(hotels), 1)
        self.assertEqual(hotels[0].hotel_id, "H001")
        self.assertGreaterEqual(mock_print.call_count, 2)

    def test_load_all_invalid_json_is_handled(self) -> None:
        self.file_path.write_text("{", encoding="utf-8")
        with patch("builtins.print") as mock_print:
            hotels = self.repo.load_all()
        self.assertEqual(hotels, [])
        self.assertTrue(
            any(
                "[DATA ERROR]" in str(call)
                for call in mock_print.call_args_list
            )
        )

    def test_load_all_non_array_root_is_handled(self) -> None:
        self.file_path.write_text(json.dumps({"a": 1}), encoding="utf-8")
        with patch("builtins.print") as mock_print:
            hotels = self.repo.load_all()
        self.assertEqual(hotels, [])
        self.assertTrue(
            any(
                "[DATA ERROR]" in str(call)
                for call in mock_print.call_args_list
            )
        )

    def test_load_all_missing_file_is_handled(self) -> None:
        self.file_path.unlink()
        with patch("builtins.print") as mock_print:
            hotels = self.repo.load_all()
        self.assertEqual(hotels, [])
        self.assertTrue(
            any(
                "[DATA WARNING]" in str(call)
                for call in mock_print.call_args_list
            )
        )

    def test_save_all_raises_persistence_error_on_os_failure(self) -> None:
        hotel = Hotel("H001", "City Inn", "MTY", 10, 10)
        with patch.object(os, "replace", side_effect=OSError("fail")):
            with self.assertRaises(PersistenceError):
                self.repo.save_all([hotel], lambda item: item.to_dict())


class TestEntityRepositories(unittest.TestCase):
    """Tests for Hotel, Customer, and Reservation repositories."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        base = Path(self.temp_dir)
        self.hotel_repo = HotelRepository(base / "hotels.json")
        self.customer_repo = CustomerRepository(base / "customers.json")
        self.reservation_repo = ReservationRepository(
            base / "reservations.json"
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_hotel_repository_crud(self) -> None:
        hotel = Hotel("H001", "City Inn", "MTY", 10, 10)
        self.hotel_repo.create_hotel(hotel)
        self.assertEqual(self.hotel_repo.get_hotel("H001").name, "City Inn")
        updated = Hotel("H001", "Beach Inn", "MTY", 10, 8)
        self.assertTrue(self.hotel_repo.update_hotel(updated))
        self.assertEqual(self.hotel_repo.get_hotel("H001").name, "Beach Inn")
        self.assertTrue(self.hotel_repo.delete_hotel("H001"))
        self.assertFalse(self.hotel_repo.delete_hotel("H001"))

    def test_hotel_repository_duplicate_raises(self) -> None:
        hotel = Hotel("H001", "City Inn", "MTY", 10, 10)
        self.hotel_repo.create_hotel(hotel)
        with self.assertRaises(DuplicateEntityError):
            self.hotel_repo.create_hotel(hotel)

    def test_customer_repository_crud(self) -> None:
        customer = Customer("C001", "Jane Doe", "jane@example.com", "555")
        self.customer_repo.create_customer(customer)
        self.assertEqual(
            self.customer_repo.get_customer("C001").full_name,
            "Jane Doe",
        )
        updated = Customer("C001", "Jane Updated", "jane@example.com", "999")
        self.assertTrue(self.customer_repo.update_customer(updated))
        self.assertEqual(self.customer_repo.get_customer("C001").phone, "999")
        self.assertTrue(self.customer_repo.delete_customer("C001"))
        self.assertFalse(self.customer_repo.delete_customer("C001"))

    def test_customer_repository_duplicate_raises(self) -> None:
        customer = Customer("C001", "Jane Doe", "jane@example.com", "555")
        self.customer_repo.create_customer(customer)
        with self.assertRaises(DuplicateEntityError):
            self.customer_repo.create_customer(customer)

    def test_reservation_repository_crud_and_cancel_paths(self) -> None:
        reservation = Reservation(
            reservation_id="R001",
            customer_id="C001",
            hotel_id="H001",
            check_in="2026-03-01",
            check_out="2026-03-03",
            num_rooms=1,
            status="active",
            created_at="2026-02-18T12:00:00",
        )
        self.reservation_repo.create_reservation(reservation)
        self.assertEqual(
            self.reservation_repo.get_reservation("R001").status,
            "active",
        )
        self.assertTrue(self.reservation_repo.cancel_reservation("R001"))
        self.assertTrue(self.reservation_repo.cancel_reservation("R001"))
        self.assertFalse(self.reservation_repo.cancel_reservation("R404"))

        updated = Reservation(
            reservation_id="R001",
            customer_id="C001",
            hotel_id="H001",
            check_in="2026-03-01",
            check_out="2026-03-04",
            num_rooms=2,
            status="cancelled",
            created_at="2026-02-18T12:00:00",
        )
        self.assertTrue(self.reservation_repo.update_reservation(updated))
        self.assertFalse(
            self.reservation_repo.update_reservation(
                Reservation(
                    reservation_id="R404",
                    customer_id="C001",
                    hotel_id="H001",
                    check_in="2026-03-01",
                    check_out="2026-03-04",
                    num_rooms=1,
                    status="active",
                    created_at="2026-02-18T12:00:00",
                )
            )
        )

    def test_reservation_repository_duplicate_raises(self) -> None:
        reservation = Reservation(
            reservation_id="R001",
            customer_id="C001",
            hotel_id="H001",
            check_in="2026-03-01",
            check_out="2026-03-03",
            num_rooms=1,
            status="active",
            created_at="2026-02-18T12:00:00",
        )
        self.reservation_repo.create_reservation(reservation)
        with self.assertRaises(DuplicateEntityError):
            self.reservation_repo.create_reservation(reservation)


if __name__ == "__main__":
    unittest.main()
