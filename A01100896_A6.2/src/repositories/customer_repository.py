"""Customer repository."""

from __future__ import annotations

from pathlib import Path

from ..exceptions import DuplicateEntityError
from ..models import Customer
from .base_json_repository import BaseJsonRepository


class CustomerRepository:
    """Manages Customer persistence operations."""

    def __init__(self, file_path: str | Path) -> None:
        self._repo = BaseJsonRepository(
            file_path, Customer.from_dict, "customer"
        )

    def create_customer(self, customer: Customer) -> None:
        customers = self._repo.load_all()
        if any(
            existing.customer_id == customer.customer_id
            for existing in customers
        ):
            raise DuplicateEntityError(
                f"customer already exists: {customer.customer_id}"
            )
        customers.append(customer)
        self._repo.save_all(customers, lambda item: item.to_dict())

    def delete_customer(self, customer_id: str) -> bool:
        customers = self._repo.load_all()
        filtered = [
            customer
            for customer in customers
            if customer.customer_id != customer_id
        ]
        deleted = len(filtered) != len(customers)
        if deleted:
            self._repo.save_all(filtered, lambda item: item.to_dict())
        return deleted

    def get_customer(self, customer_id: str) -> Customer | None:
        for customer in self._repo.load_all():
            if customer.customer_id == customer_id:
                return customer
        return None

    def get_all_customers(self) -> list[Customer]:
        return self._repo.load_all()

    def update_customer(self, customer: Customer) -> bool:
        customers = self._repo.load_all()
        updated = False
        for idx, current in enumerate(customers):
            if current.customer_id == customer.customer_id:
                customers[idx] = customer
                updated = True
                break
        if updated:
            self._repo.save_all(customers, lambda item: item.to_dict())
        return updated
