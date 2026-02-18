# Hotel Reservation System - Design Document

## 1. Objective
Design a Python-based system with three main abstractions:
- `Hotel`
- `Customer`
- `Reservation`

The system must support create, delete, display, and modify operations, plus room reservation and cancellation, with persistence in files.

## 2. Scope and Assumptions
- Persistence will be file-based using JSON files.
- Each entity has a unique ID.
- Dates use ISO format: `YYYY-MM-DD`.
- A reservation is valid only if room capacity is available for the requested period.

## 3. High-Level Architecture
- **Domain layer**: classes for `Hotel`, `Customer`, `Reservation`.
- **Persistence layer**: repository classes to read/write JSON files.
- **Service layer**: business operations requested in requirements.

## 4. Data Model

### 4.1 Hotel
Proposed attributes:
- `hotel_id: str`
- `name: str`
- `location: str`
- `total_rooms: int`
- `available_rooms: int`
- `rating: float` (optional)
- `active: bool`

### 4.2 Customer
Proposed attributes:
- `customer_id: str`
- `full_name: str`
- `email: str`
- `phone: str`
- `active: bool`

### 4.3 Reservation
Proposed attributes:
- `reservation_id: str`
- `customer_id: str`
- `hotel_id: str`
- `check_in: str` (`YYYY-MM-DD`)
- `check_out: str` (`YYYY-MM-DD`)
- `num_rooms: int`
- `status: str` (`active`, `cancelled`)
- `created_at: str` (timestamp)

## 5. Persistence Design

### 5.1 Files
- `data/hotels.json`
- `data/customers.json`
- `data/reservations.json`

### 5.2 Storage format
Each file stores a JSON array of objects.

Example (`hotels.json`):
```json
[
  {
    "hotel_id": "H001",
    "name": "City Inn",
    "location": "Monterrey",
    "total_rooms": 100,
    "available_rooms": 98,
    "rating": 4.2,
    "active": true
  }
]
```

## 6. Class and Method Design

### 6.1 Domain Classes
- `class Hotel`
  - `to_dict() -> dict`
  - `from_dict(data: dict) -> Hotel`

- `class Customer`
  - `to_dict() -> dict`
  - `from_dict(data: dict) -> Customer`

- `class Reservation`
  - `to_dict() -> dict`
  - `from_dict(data: dict) -> Reservation`

### 6.2 Repository Classes
- `class HotelRepository`
  - `create_hotel(hotel: Hotel) -> None`
  - `delete_hotel(hotel_id: str) -> bool`
  - `get_hotel(hotel_id: str) -> Hotel | None`
  - `get_all_hotels() -> list[Hotel]`
  - `update_hotel(hotel: Hotel) -> bool`

- `class CustomerRepository`
  - `create_customer(customer: Customer) -> None`
  - `delete_customer(customer_id: str) -> bool`
  - `get_customer(customer_id: str) -> Customer | None`
  - `get_all_customers() -> list[Customer]`
  - `update_customer(customer: Customer) -> bool`

- `class ReservationRepository`
  - `create_reservation(reservation: Reservation) -> None`
  - `cancel_reservation(reservation_id: str) -> bool`
  - `get_reservation(reservation_id: str) -> Reservation | None`
  - `get_all_reservations() -> list[Reservation]`
  - `update_reservation(reservation: Reservation) -> bool`

### 6.3 Service Layer (Required Behaviors)

#### Hotels
- `create_hotel(...)`
- `delete_hotel(hotel_id)`
- `display_hotel_info(hotel_id)`
- `modify_hotel_info(hotel_id, **changes)`
- `reserve_room(customer_id, hotel_id, check_in, check_out, num_rooms)`
- `cancel_reservation(reservation_id)`

#### Customers
- `create_customer(...)`
- `delete_customer(customer_id)`
- `display_customer_info(customer_id)`
- `modify_customer_info(customer_id, **changes)`

#### Reservations
- `create_reservation(customer_id, hotel_id, check_in, check_out, num_rooms)`
- `cancel_reservation(reservation_id)`

Note: `reserve_room(...)` in Hotels can internally call `create_reservation(...)`.

## 7. Key Validation Rules
- IDs must be unique.
- `total_rooms >= 0`, `available_rooms >= 0`, `num_rooms > 0`.
- `check_out > check_in`.
- Hotel and customer must exist and be active.
- Reservation creation must fail if available rooms are insufficient.
- Cancelling a reservation restores room availability.

## 8. Error Handling
Use custom exceptions:
- `EntityNotFoundError`
- `ValidationError`
- `DuplicateEntityError`
- `PersistenceError`

### 8.1 Invalid Data in Files (Req 5)
The system must continue execution even when file data is partially invalid.

Design decisions:
- Repositories load data record-by-record, not as all-or-nothing processing.
- If one record is malformed (missing fields, wrong type, invalid date, invalid JSON object shape), that record is skipped.
- A clear error message is printed to console including:
  - file name
  - record index or identifier (if available)
  - reason for failure
- Valid records are still returned and can be used by the program.

Example console message format:
`[DATA ERROR] file=reservations.json record=15 reason=check_out must be later than check_in`

### 8.2 Repository Behavior for Resilience
- `get_all_hotels()`, `get_all_customers()`, and `get_all_reservations()` return only valid entities.
- If a file is missing, return an empty list and print a warning to console.
- If a file has invalid JSON syntax:
  - print an error to console
  - continue execution with an empty list for that file
- Write operations (`create`, `update`, `delete`, `cancel`) must preserve valid existing data and avoid crashing due to unrelated invalid records.

## 9. Suggested Project Structure
```text
A01100896_A6.2/
  design/
    design_document.md
  src/
    models/
      hotel.py
      customer.py
      reservation.py
    repositories/
      hotel_repository.py
      customer_repository.py
      reservation_repository.py
    services/
      reservation_service.py
    exceptions.py
  data/
    hotels.json
    customers.json
    reservations.json
```

## 10. Minimal End-to-End Flow
1. Create `Customer` and `Hotel`.
2. Call `create_reservation(customer_id, hotel_id, check_in, check_out, num_rooms)`.
3. Service validates input and availability.
4. Reservation is stored in `reservations.json`.
5. Hotel availability is updated in `hotels.json`.
6. On cancellation, reservation status becomes `cancelled` and rooms are released.

## 11. Non-Functional Considerations
- Keep read/write operations atomic per file update.
- Add simple logging for create/update/delete actions.
- Prepare method signatures to enable migration to DB later.
