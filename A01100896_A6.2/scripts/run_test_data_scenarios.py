"""Run valid and invalid CRUD/reservation scenarios from test_data."""
# pylint: disable=import-error,wrong-import-position

from __future__ import annotations

import json
import sys
import traceback
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.services.hotel_reservation_system import (  # noqa: E402
    HotelReservationSystem,
)

BASE_DIR = PROJECT_ROOT
TEST_DATA_DIR = BASE_DIR / "test_data"
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results" / "execution_runs"


def load_json(path: Path) -> dict:
    """Load and return JSON content from a file path."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def reset_persistent_data() -> None:
    """Reset persistent entity files to empty arrays."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for filename in ("hotels.json", "customers.json", "reservations.json"):
        (DATA_DIR / filename).write_text("[]\n", encoding="utf-8")


def read_persistent_snapshot() -> dict[str, str]:
    """Return current persisted data content for each entity file."""
    snapshot: dict[str, str] = {}
    for filename in ("hotels.json", "customers.json", "reservations.json"):
        file_path = DATA_DIR / filename
        snapshot[filename] = file_path.read_text(encoding="utf-8").strip()
    return snapshot


# pylint: disable=too-many-locals,too-many-branches,too-many-statements
def run_once(scenario: str) -> None:
    """Execute one scenario (valid or invalid) and write results."""
    hotels_data = load_json(TEST_DATA_DIR / f"{scenario}_hotels.json")
    customers_data = load_json(TEST_DATA_DIR / f"{scenario}_customers.json")
    reservations_data = load_json(
        TEST_DATA_DIR / f"{scenario}_reservations.json"
    )

    service = HotelReservationSystem(DATA_DIR)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_file = RESULTS_DIR / f"{scenario}_run_results.txt"

    lines: list[str] = []
    created_reservation_ids: list[str] = []
    snapshot_before = read_persistent_snapshot()

    def explain_result(label: str, result: object) -> str:
        """Return a readable explanation for common operation outputs."""
        detail = f"result={result}"
        if label.startswith("Display Hotel") and result is None:
            detail = "Hotel does not exist"
        elif label.startswith("Display Customer") and result is None:
            detail = "Customer does not exist"
        elif label.startswith("Display Reservation") and result is None:
            detail = "Reservation does not exist"
        elif label.startswith("Modify Hotel") and result is False:
            detail = "Hotel does not exist; nothing modified"
        elif label.startswith("Modify Customer") and result is False:
            detail = "Customer does not exist; nothing modified"
        elif label.startswith("Delete Hotel") and result is False:
            detail = "Hotel does not exist; nothing deleted"
        elif label.startswith("Delete Customer") and result is False:
            detail = "Customer does not exist; nothing deleted"
        elif label.startswith("Cancel Reservation") and result is False:
            detail = "Reservation does not exist; nothing cancelled"
        elif (
            label.startswith("Create Reservation")
            and isinstance(result, dict)
        ):
            reservation_id = result.get("reservation_id", "N/A")
            detail = f"Reservation created with id={reservation_id}"
        elif result is None and label.startswith("Create "):
            detail = "Created successfully"
        elif result is True:
            detail = "Operation completed successfully"
        return detail

    def execute(label: str, expected: str, func, *args, **kwargs):
        """Execute an operation and log expected-vs-actual outcome."""
        result = None
        try:
            result = func(*args, **kwargs)
            detail = explain_result(label, result)
            if expected == "FAIL" and result is False:
                lines.append(
                    f"FAIL | EXPECTED={expected} | MATCH=YES | {label} "
                    f"| {detail}"
                )
                return result
            if expected == "FAIL":
                lines.append(
                    f"FAIL | EXPECTED={expected} | MATCH=NO  | {label} "
                    f"| unexpected {detail}"
                )
            else:
                lines.append(
                    f"PASS | EXPECTED={expected} | MATCH=YES | {label} "
                    f"| {detail}"
                )
            return result
        except Exception as exc:  # pylint: disable=broad-exception-caught
            if expected == "FAIL":
                lines.append(
                    f"FAIL | EXPECTED={expected} | MATCH=YES | {label} "
                    f"| {type(exc).__name__}: {exc}"
                )
            else:
                lines.append(
                    f"FAIL | EXPECTED={expected} | MATCH=NO  | {label} "
                    f"| {type(exc).__name__}: {exc}"
                )
        return result

    lines.append(
        f"Scenario {scenario} started: "
        f"{datetime.now().isoformat(timespec='seconds')}"
    )

    # Hotel operations
    for hotel in hotels_data["create"]:
        expected = "PASS" if scenario == "valid" else "FAIL"
        execute(
            f"Create Hotel {hotel.get('hotel_id')}",
            expected,
            service.create_hotel,
            **hotel,
        )

    for hotel_id in hotels_data["display"]:
        execute(
            f"Display Hotel {hotel_id}",
            "PASS",
            service.display_hotel_info,
            hotel_id,
        )

    for mod in hotels_data["modify"]:
        execute(
            f"Modify Hotel {mod['hotel_id']}",
            "PASS",
            service.modify_hotel_info,
            mod["hotel_id"],
            **mod["changes"],
        )

    # Customer operations
    for customer in customers_data["create"]:
        expected = "PASS" if scenario == "valid" else "FAIL"
        execute(
            f"Create Customer {customer.get('customer_id')}",
            expected,
            service.create_customer,
            **customer,
        )

    for customer_id in customers_data["display"]:
        execute(
            f"Display Customer {customer_id}",
            "PASS",
            service.display_customer_info,
            customer_id,
        )

    for mod in customers_data["modify"]:
        execute(
            f"Modify Customer {mod['customer_id']}",
            "PASS",
            service.modify_customer_info,
            mod["customer_id"],
            **mod["changes"],
        )

    # Reservation operations
    for index, reservation in enumerate(reservations_data["create"]):
        expected = "PASS" if scenario == "valid" else "FAIL"
        label = (
            "Create Reservation "
            f"{reservation['customer_id']}->{reservation['hotel_id']}"
        )
        if index == 0:
            result = execute(
                label, expected, service.reserve_room, **reservation
            )
        else:
            result = execute(
                label,
                expected,
                service.create_reservation,
                **reservation,
            )

        if isinstance(result, dict) and result.get("reservation_id"):
            created_reservation_ids.append(result["reservation_id"])

    for reservation_id in reservations_data["cancel"]:
        resolved_id = reservation_id
        if reservation_id == "<created_first>" and created_reservation_ids:
            resolved_id = created_reservation_ids[0]
        expected = "PASS" if scenario == "valid" else "FAIL"
        execute(
            f"Cancel Reservation {resolved_id}",
            expected,
            service.cancel_reservation,
            resolved_id,
        )

    # Delete entities after reservation cancellations
    for customer_id in customers_data["delete"]:
        execute(
            f"Delete Customer {customer_id}",
            "PASS",
            service.delete_customer,
            customer_id,
        )

    for hotel_id in hotels_data["delete"]:
        execute(
            f"Delete Hotel {hotel_id}",
            "PASS",
            service.delete_hotel,
            hotel_id,
        )

    snapshot_after = read_persistent_snapshot()
    changed = snapshot_before != snapshot_after
    if scenario != "invalid" or changed:
        lines.append("")
        lines.append("Persistent data snapshot after run:")
        for filename in ("hotels.json", "customers.json", "reservations.json"):
            lines.append(f"- {filename}: {snapshot_after[filename]}")

    output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    """Run both scenarios and persist execution outputs."""
    try:
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        for file_path in RESULTS_DIR.glob("*.txt"):
            file_path.unlink()
        reset_persistent_data()
        run_once("valid")
        run_once("invalid")
    except Exception:  # pylint: disable=broad-exception-caught
        error_file = RESULTS_DIR / "runner_error.txt"
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        error_file.write_text(traceback.format_exc(), encoding="utf-8")
        raise


if __name__ == "__main__":
    main()
