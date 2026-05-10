from __future__ import annotations

from collections.abc import Callable
from threading import Lock
from typing import Any


class TokenManager:
    _token: str | None = None
    _login_fn: Callable[[], str] | None = None
    _lock = Lock()

    @classmethod
    def register_login(cls, func: Callable[[], str]) -> None:
        cls._login_fn = func

    @classmethod
    def set_token(cls, token: str | None) -> None:
        with cls._lock:
            cls._token = token

    @classmethod
    def clear(cls) -> None:
        with cls._lock:
            cls._token = None

    @classmethod
    def get_token(cls) -> str:
        with cls._lock:
            if cls._token:
                return cls._token
        if cls._login_fn is None:
            raise RuntimeError("TokenManager: no login function registered")
        token = cls._login_fn()
        with cls._lock:
            cls._token = token
        return token
