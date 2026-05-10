from __future__ import annotations

from typing import Any


class Context:
    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def update(self, other: dict[str, Any]) -> None:
        self._data.update(other)

    def clear(self) -> None:
        self._data.clear()

    @property
    def data(self) -> dict[str, Any]:
        return self._data
