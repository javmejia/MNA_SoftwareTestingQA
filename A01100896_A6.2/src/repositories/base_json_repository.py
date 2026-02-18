"""Base repository helpers for JSON persistence."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Callable, Generic, TypeVar

from ..exceptions import PersistenceError, ValidationError

T = TypeVar("T")


class BaseJsonRepository(Generic[T]):
    """Generic repository for file-based JSON persistence."""

    def __init__(
        self,
        file_path: str | Path,
        entity_factory: Callable[[dict], T],
        entity_name: str,
    ) -> None:
        self.file_path = Path(file_path)
        self.entity_factory = entity_factory
        self.entity_name = entity_name
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write_raw([])

    def _write_raw(self, data: list[dict]) -> None:
        try:
            with tempfile.NamedTemporaryFile(
                "w",
                encoding="utf-8",
                dir=str(self.file_path.parent),
                delete=False,
            ) as temp_file:
                json.dump(data, temp_file, indent=2, ensure_ascii=True)
                temp_file_path = temp_file.name
            os.replace(temp_file_path, self.file_path)
        except OSError as exc:
            raise PersistenceError(
                f"failed writing file: {self.file_path}"
            ) from exc

    def _load_raw(self) -> list[dict]:
        if not self.file_path.exists():
            print(
                f"[DATA WARNING] file={self.file_path.name} "
                "reason=file does not exist"
            )
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                content = json.load(file)
        except json.JSONDecodeError as exc:
            print(
                f"[DATA ERROR] file={self.file_path.name} "
                f"reason=invalid JSON syntax ({exc.msg})"
            )
            return []
        except OSError as exc:
            raise PersistenceError(
                f"failed reading file: {self.file_path}"
            ) from exc

        if not isinstance(content, list):
            print(
                f"[DATA ERROR] file={self.file_path.name} "
                "reason=root must be a JSON array"
            )
            return []
        return content

    def load_all(self) -> list[T]:
        """Load all valid entities, skipping invalid records."""
        entities: list[T] = []
        for idx, record in enumerate(self._load_raw()):
            if not isinstance(record, dict):
                print(
                    f"[DATA ERROR] file={self.file_path.name} "
                    f"record={idx} reason=record must be an object"
                )
                continue
            try:
                entities.append(self.entity_factory(record))
            except ValidationError as exc:
                print(
                    f"[DATA ERROR] file={self.file_path.name} "
                    f"record={idx} reason={exc}"
                )
        return entities

    def save_all(
        self, entities: list[T], serializer: Callable[[T], dict]
    ) -> None:
        """Save all entities to disk."""
        data = [serializer(entity) for entity in entities]
        self._write_raw(data)
